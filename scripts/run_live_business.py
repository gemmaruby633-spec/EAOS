import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from packages.self_hosting.application.agency_orchestrator import (  # noqa: E402
    SolopreneurAgencyOrchestrator,
)

# Initialize Agency Orchestrator
orchestrator = SolopreneurAgencyOrchestrator()

# Execute Real Customer Order & Content Generation Run
result = orchestrator.execute_end_to_end_business_run(
    topic_keyword="Tu dong hoa Doanh nghiep AI",
    customer_email="khachhang@doanhnghiep.com",
    product_id="PROD-AI-AUTOMATION-KIT",
    sale_amount_usd=199.0,
    ai_cost_usd=0.15,
)

print("\n----------------------------------------------------")
print(" BÁO CÁO KẾT QUẢ VẬN HÀNH DOANH NGHIỆP THỰC TẾ      ")
print("----------------------------------------------------")
print(f"1. Mã Giao dịch        : {result.execution_id}")
print(f"2. Từ khóa SEO Đã quét : {result.keyword_researched}")
print(f"3. Bài viết SEO Sinh ra : {result.article_slug}.md")
print(f"4. Khách hàng Lead CRM  : {result.lead_captured_email}")
print(f"5. Doanh thu Bán hàng  : ${result.order_amount_usd} USD")
print(f"6. Chi phí Vận hành AI : ${result.ai_cost_usd} USD")
print(f"7. LỢI NHUẬN RÒNG (P&L): ${result.net_profit_usd} USD")
print(f"8. Tỷ lệ Lợi nhuận ROI  : {result.roi_percentage}%")
print(f"9. Trôi Kiến trúc      : {result.architecture_drift} (0.00 Clean)")
print("----------------------------------------------------")
