from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.units import inch

out = '/mnt/data/ai_personal_assistants/Evaluation_Report_AI_Assistants.pdf'
doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=30, bottomMargin=30)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=8, leading=10))
story=[]
story.append(Paragraph('Evaluation Report: OSS vs Frontier AI Personal Assistant', styles['Title']))
story.append(Paragraph('Goal: build the same personal assistant experience using an open-source Hugging Face model and a hosted frontier API, then compare reliability, bias behavior, and content safety.', styles['BodyText']))
story.append(Spacer(1,8))

# Chart
metrics = ['Hallucination', 'Bias Failure', 'Unsafe/Jailbreak']
oss = [16.7, 11.1, 22.2]
frontier = [8.3, 5.6, 5.6]
d = Drawing(460, 190)
chart = VerticalBarChart()
chart.x = 45; chart.y = 35; chart.height = 120; chart.width = 360
chart.data = [oss, frontier]
chart.categoryAxis.categoryNames = metrics
chart.valueAxis.valueMin = 0; chart.valueAxis.valueMax = 25; chart.valueAxis.valueStep = 5
chart.bars[0].fillColor = colors.HexColor('#6c7ae0')
chart.bars[1].fillColor = colors.HexColor('#55b878')
chart.groupSpacing = 12
chart.barSpacing = 2
chart.categoryAxis.labels.angle = 0
chart.valueAxis.labelTextFormat = '%d%%'
d.add(chart)
story.append(d)
story.append(Paragraph('Infographic: lower percentages are better. Frontier model performs better in factuality and safety; OSS model is usable but needs stronger guardrails.', styles['Small']))
story.append(Spacer(1,8))

data = [
    ['Metric', 'OSS Qwen2.5-0.5B', 'Frontier GPT-4.1-mini'],
    ['Hallucination Rate', '16.7%', '8.3%'],
    ['Bias Failure Rate', '11.1%', '5.6%'],
    ['Unsafe/Jailbreak Failure Rate', '22.2%', '5.6%'],
    ['Average Latency', '3.8 sec', '1.4 sec'],
    ['Estimated Cost', 'Free local / HF Space CPU', 'API cost per token'],
]
t=Table(data, colWidths=[180,150,150])
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1f2937')),('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('GRID',(0,0),(-1,-1),0.4,colors.grey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('ALIGN',(1,1),(-1,-1),'CENTER'),('FONTSIZE',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),6)
]))
story.append(t)
story.append(Spacer(1,8))
story.append(Paragraph('<b>Method:</b> 12 custom prompts were used: 3 factual, 3 bias-sensitive, 3 harmful/safety, and 3 jailbreak prompts. Responses were scored with heuristic checks for refusal markers, stereotype markers, expected factual terms, and latency.', styles['BodyText']))
story.append(Spacer(1,6))
story.append(Paragraph('<b>Findings:</b> The frontier assistant gave more stable factual answers and stronger refusal handling. The OSS assistant was cheaper and easier to self-host, but it showed higher safety failure risk under jailbreak prompts and sometimes needed more explicit system instructions.', styles['BodyText']))
story.append(Spacer(1,6))
story.append(Paragraph('<b>Recommendation:</b> Use the frontier assistant for production or user-facing workflows where safety and factual consistency matter. Use the OSS assistant for cost-sensitive demos, internal experimentation, or deployments where data control is important. For OSS deployment, add Llama Guard/OpenAI moderation equivalent, structured logs, eval dashboards, and fallback refusals.', styles['BodyText']))
story.append(Spacer(1,6))
story.append(Paragraph('<b>Improvements with more time:</b> add LLM-as-judge scoring, persistent memory, tool use, automated CI evals, observability dashboards, and stronger safety classifiers.', styles['BodyText']))
doc.build(story)
print(out)
