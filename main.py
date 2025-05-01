from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_blog_post(input_text: str):
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(
        inputs["input_ids"],
        max_length=500,
        num_beams=5,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

def create_blog_template(title, author, rating, link):
    return f"""
    # {title}: A Must-Read Book for Everyone

    **Author:** {author}

    **Rating:** {rating}

    **Link:** [Click here to check out the book on Amazon]({link})

    ## Introduction
    {title} by {author} is one of the top books currently trending. With an impressive rating of {rating}, this book has captured the attention of readers worldwide. Whether you're an avid reader or new to the genre, {title} offers something valuable to everyone.

    ## Why You Should Read {title}
    {title} is not just a book; it's an experience. The author, {author}, has skillfully crafted a narrative that resonates with readers on a deep level. The compelling storyline, coupled with exceptional character development, makes this book a page-turner.

    ## Key Highlights
    - **Incredible Storyline**: {title} offers a unique narrative that keeps readers engaged.
    - **Engaging Characters**: The characters in {title} are relatable and well-developed.
    - **High Rating**: The book has received outstanding reviews, with a rating of {rating}, reflecting its popularity and quality.

    ## Conclusion
    {title} is a must-read for anyone looking to dive into a world of captivating storytelling. With a high rating and positive reviews, it's no wonder this book has become a bestseller. Don't miss out—[check it out now on Amazon]({link})!

    Happy reading!
    """

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    url = "https://www.amazon.com/Best-Sellers-Books/zgbs/books"
    driver.get(url)

    time.sleep(3)

    product = driver.find_element(By.CSS_SELECTOR, ".zg-grid-general-faceout")

    title = product.find_element(By.CSS_SELECTOR, "img").get_attribute("alt")
    link = product.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href")

    try:
        author = product.find_element(By.CSS_SELECTOR, ".a-row.a-size-small").text
    except:
        author = "N/A"

    try:
        rating = product.find_element(By.CSS_SELECTOR, ".a-icon-alt").text
    except Exception as e:
        print("Rating not found or unavailable:", e)
        rating = "N/A"

    print("Title:", title)
    print("Author:", author)
    print("Rating:", rating)
    print("URL:", link)

    blog_post = create_blog_template(title, author, rating, link)

    enhanced_blog_post = generate_blog_post(blog_post)
    print("\nGenerated Blog Post:")
    print(enhanced_blog_post)

finally:
    driver.quit()
