# Quick Start Guide 🚀

Get up and running with the Person Search Tool in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
cd /Users/raiymbek/Desktop/chatgpt
pip install -r requirements.txt
```

## Step 2: Optional - Get API Key (Optional, 2 minutes)

For better results, sign up for a free Tavily API key:

1. Go to [https://tavily.com/](https://tavily.com/)
2. Sign up for free (1,000 searches/month - 10x more than alternatives!)
3. Copy your API key from the dashboard
4. Create a `.env` file:
   ```bash
   echo "TAVILY_API_KEY=your_actual_key_here" > .env
   ```

**Why Tavily?** It's specifically designed for AI agents with better quality results, relevance scoring, and content extraction.

**Skip this step if you want to try basic search first.**

## Step 3: Run Your First Search (30 seconds)

### Option A: Run the example (simplest)
```bash
python example_search.py
```

### Option B: Run the main script
```bash
python person_search.py
```

### Option C: Search for someone else
Edit `person_search.py` and change:
```python
person_name = "Your Person Name"
university = "Their University"  # or None
```

Then run:
```bash
python person_search.py
```

## What You'll Get

The tool will search for:
- 📚 **Academic papers** (Google Scholar, arXiv)
- 📰 **News articles** (Google News, university news)
- 🌐 **Web mentions** (general search, podcasts, interviews)

Results will be:
- Displayed in your console with nice formatting
- Saved to a JSON file (e.g., `search_results_aruzhan_abil_20241109_103000.json`)

## Example Output

```
================================================================================
📊 SEARCH SUMMARY FOR: Aruzhan Abil
================================================================================

🎓 Academic Papers: 3
   • Google Scholar: 2
   • Arxiv: 1

📰 News Articles: 2
   • Google News: 1
   • University News: 1

🌐 Web Results: 5
   • General Search: 5

================================================================================
```

## Customize Your Search

Create your own search script:

```python
from person_search import PersonSearcher

# Initialize
searcher = PersonSearcher(tavily_api_key="your_key_or_None")

# Search
results = searcher.search(
    person_name="Jane Doe",
    university="MIT",
    max_results_per_source=10,
    search_papers=True,
    search_news=True,
    search_web=True
)

# Display
searcher.print_summary(results)
searcher.print_detailed_results(results)
searcher.save_results(results)
```

## Troubleshooting

### Problem: "No module named 'scholarly'"
**Solution:** 
```bash
pip install -r requirements.txt
```

### Problem: Very few or no results
**Solutions:**
- Try with a Tavily API key (much better results - 1,000 free searches/month!)
- Try different name variations
- Check if the person has online presence
- Increase `max_results_per_source`

### Problem: "Google Scholar blocked the request"
**Solution:** 
- Wait 5-10 minutes and try again
- Use a VPN
- This mainly affects paper searches; web search with Tavily API is not affected

## Next Steps

1. ✅ Read the full [README.md](README.md) for detailed documentation
2. ✅ Check out [example_search.py](example_search.py) for more examples
3. ✅ Customize [config_example.py](config_example.py) for your needs

## Need Help?

- Check [README.md](README.md) - Troubleshooting section
- Review [example_search.py](example_search.py) - Multiple examples
- Check the inline code comments

---

**Happy searching! 🔍**

