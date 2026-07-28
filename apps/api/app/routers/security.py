"""Security and SOC Hardening router."""

from typing import Annotated, Any
from fastapi import APIRouter, Body
from platform_services.cache.redis_rate_limiter import RedisDistributedRateLimiter
from platform_services.database.circuit_breaker_pool import DatabaseCircuitBreakerPool
from platform_services.security.cloudflare_waf_driver import CloudflareWAFDriver
from platform_services.security.post_quantum_signer import PostQuantumSignerEngine, ZKAttestationProof
from platform_services.security.quantum_envelope import EncryptedEnvelopeDTO, QuantumEnvelopeEncryptionEngine
from platform_services.security.wazuh_mtls_adapter import WazuhMTLSSyslogAdapter

router = APIRouter(prefix="/security", tags=["Security"])

global_waf_driver = CloudflareWAFDriver()
global_syslog_adapter = WazuhMTLSSyslogAdapter()
quantum_engine = QuantumEnvelopeEncryptionEngine()


@router.post("/quantum/encrypt-envelope", response_model=EncryptedEnvelopeDTO, status_code=201)
async def encrypt_quantum_envelope(request: dict[str, Any] | None = None) -> EncryptedEnvelopeDTO:
    return quantum_engine.encrypt_secret_payload(secret_data="secret", public_key_fingerprint="kyber768_fp")


@router.post("/wazuh/syslog-hmac")
async def sign_wazuh_syslog_payload(request: dict[str, Any] | None = None) -> Any:
    return global_syslog_adapter.format_signed_syslog(log_data={}, secret_key="default_secret")


@router.post("/cloudflare/block-cooldown")
async def block_cloudflare_ip_cooldown(request: dict[str, Any] | None = None) -> Any:
    return global_waf_driver.block_ip_with_cooldown(ip="203.0.113.50", ttl_seconds=1800)


@router.post("/wazuh/stream-event")
async def stream_wazuh_siem_event(event_payload: dict[str, Any]) -> dict[str, Any]:
    alert = global_syslog_adapter.stream_audit_event(event_payload)
    return {"status": "STREAMED", "alert": alert.model_dump()}


@router.post("/cloudflare/block-ip")
async def block_cloudflare_ip(ip_address: Annotated[str, Body(embed=True)]) -> dict[str, Any]:
    rule = global_waf_driver.block_malicious_ip(ip_address)
    return {"status": "BLOCKED", "rule": rule.model_dump()}


@router.post("/vault/rotate-secret")
async def rotate_vault_ephemeral_secret(request: dict[str, Any] | None = None) -> dict[str, Any]:
    from platform_services.security.vault_ephemeral import VaultEphemeralSigner

    signer = VaultEphemeralSigner()
    return signer.generate_ephemeral_token(secret_path="secret/data/db", ttl_sec=900).model_dump()


@router.post("/zkp/attest-proof")
async def generate_zkp_attest_proof(request: dict[str, Any] | None = None) -> ZKAttestationProof:
    signer = PostQuantumSignerEngine()
    return signer.generate_compliance_proof(artifact_id="artifact_1", payload_data="dummy")


@router.post("/rate-limit/redis")
def check_rate_limit(client_ip: str = "127.0.0.1") -> Any:
    return RedisDistributedRateLimiter().check_rate_limit(client_ip)


@router.get("/circuit-breaker/health")
def db_health() -> Any:
    return DatabaseCircuitBreakerPool().get_pool_health()
