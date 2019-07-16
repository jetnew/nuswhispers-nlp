from classes import Post, Collection
from selenium import webdriver

# Open browser
driver = webdriver.Chrome()

# # Create sample post
# post = Post(65313)
# post.get_text(driver)
# print(post.text)

# Create collection
collection = Collection()
for tag in range(65799, -1, -1):
    post = Post(tag)
    post.get_text(driver)
    print("Tag:", tag, '-', post.has_text())
    collection.insert(post)

    if tag % 100 == 0:
        # Save collection
        collection.to_df()
        collection.to_csv('collection'+str(tag//100)+'.csv')
        collection.to_excel('collection'+str(tag//100)+'.xlsx')
        collection = Collection()

# Close browser
driver.close()
