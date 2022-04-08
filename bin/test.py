from pprint import pprint
from notion_client import Client

notion =Client(auth="secret_xPnqQflGU4dJKUQ3zUbGTXOgNyGCYpThjjqzwQ71wSy")
DB_ID = "e0c91e19c9a747e7b497d2535341fc17"
properties = {
    "Title": {"title": [{"text": {"content": "IT Systems Engineer"} }]},
    "First Name": {"type": "rich_text", "rich_text": [{"text": {"content": "Marshall"} }]},
    "Last Name": {"type": "rich_text", "rich_text": [{"text": {"content": "Amey"} }]},
    "Work Email": {"type": "email", "email": "mamey@4catalyzer.com"},
    "Personal Email": {"type": "email", "email": "mj@marshallamey.com"},
    "Manager": {"type": "rich_text", "rich_text": [{"text": {"content": "Alan McKenna"} }]},
}
pprint(properties)

# notion.pages.update(
#     page_id="e9aad0378e314787babc55a752d55ead",
#     properties=properties
# )

currentUser = notion.databases.query(DB_ID, filter={"property": "Work Email", "email": { "equals": "mamey@4catalyzer.com"}})
pprint(currentUser)