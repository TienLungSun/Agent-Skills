import yaml
import os

def analyze_sentiment(text):
    # 簡易情感分析邏輯 (可擴充串接 OpenAI API)
    negative_words = ['差', '慢', '貴', '詐騙', '難用', '不要買']
    score = sum(1 for word in negative_words if word in text)
    return "Negative" if score > 0 else "Positive"

def run_agent():
    print("🚀 輿情分析 Agent 啟動中...")
    
    # 讀取設定
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    brand = config['settings']['brand_name']
    sources = config['data_sources'][0]['content']
    threshold = config['settings']['alert_threshold']
    
    results = []
    neg_count = 0

    print(f"📊 正在分析關於 [{brand}] 的評論...")
    
    for comment in sources:
        sentiment = analyze_sentiment(comment)
        if sentiment == "Negative":
            neg_count += 1
        results.append({"text": comment, "sentiment": sentiment})
    
    neg_ratio = neg_count / len(sources)
    
    # 輸出報告
    print("\n--- 分析報告 ---")
    for r in results:
        icon = "🔴" if r['sentiment'] == "Negative" else "🟢"
        print(f"{icon} {r['text']}")
    
    print(f"\n負面聲量比例: {neg_ratio*100}%")
    
    if neg_ratio >= threshold:
        print("⚠️ [警報] 負面聲量已達臨界值，請公關團隊介入！")
    else:
        print("✅ 目前輿情穩定。")

if __name__ == "__main__":
    run_agent()