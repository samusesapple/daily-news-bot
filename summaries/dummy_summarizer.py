from typing import List
from summaries.news_summarizer import SummaryResult, KeywordDetail, Summarizer

class DummySummarizer(Summarizer):
    def summarize(self, text: str) -> SummaryResult:
        keywords = ["신탁", "환율", "금리"]
        keyword_details = {
            "신탁": KeywordDetail(
                explanation="제3자가 대신 보관하는 계약",
                example="자산을 신탁회사에 맡겼다."
            ),
            "환율": KeywordDetail(
                explanation="외국 돈과 우리 돈의 교환 비율",
                example="환율이 급등했다."
            ),
            "금리": KeywordDetail(
                explanation="돈을 빌릴 때 적용되는 이자율",
                example="금리가 인상되었다."
            ),
        }
        return SummaryResult(
            summary="전세 사기 피해가 반복되고 있으며 정부는 대책을 논의 중이다.",
            keywords=keywords,
            keyword_details=keyword_details
        ) 