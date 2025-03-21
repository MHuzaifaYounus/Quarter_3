import streamlit as st
from pymongo import MongoClient


client  = MongoClient("mongodb+srv://huzaifa:king1452007@librarymanager.jxrpp.mongodb.net/?retryWrites=true&w=majority&appName=LibraryManager")
db = client["library_db"]
collection = db["books"]

def add_book(book):
    try:
        result = collection.insert_one(book)
        return True
    except Exception as e:
        return False , str(e)

def remove_book(title):
    try:
        result = collection.delete_one({"title": title})
        return True
    except Exception as e:
        return False

def view_books():
    try:
        books = collection.find()
        return list(books)
    except Exception as e:
        return []

def mark_as_read(query):
    try:
        for book in collection.find():
            if query.lower() in book["title"].lower():
                collection.update_one({"title": query}, {"$set": {"status": "Read"}})
                return True
            elif query.lower() in book["author"].lower():
                collection.update_one({"author": query}, {"$set": {"status": "Read"}})
                return True
        return False
    except Exception as e:
        return False

def display_statistics():
    try:
        total_books = collection.count_documents({})
        read_books = collection.count_documents({"status": "Read"})
        unread_books = collection.count_documents({"status": "Unread"})
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        
        return {
            "total": total_books,
            "read": read_books,
            "unread": unread_books,
            "percent_read": round(percentage_read, 1)
        }
    except Exception as e:
        return {
            "total": 0,
            "read": 0, 
            "unread": 0,
            "percent_read": 0
        }

st.title("📚 Library Management System")

st.sidebar.title("📋 Menu")
page = st.sidebar.radio("Select a page", ["📕 Add a Book", "🗑️ Remove a Book", "📚 View Books", "🔍 Search Books","✅ Mark as Read","📊 Display Statistics"])

if page == "📕 Add a Book":
    st.subheader("📕 Add a Book")
    title = st.text_input("📝 Title",key="title_input")
    author = st.text_input("✍️ Author",key="author_input")
    year = st.number_input("📅 Publication Year",min_value=1000,key="year_input")
    status = st.radio("📖 Status", ["Read", "Unread"],key="status_input")
    if st.button("➕ Add Book",key="add_button"):
        result = add_book({"title":title,"author":author,"year":year,"status":status})
        if result:
            st.success("✅ Book added successfully")
        else:
            st.error(f"❌ Failed to add book: {result}")

elif page == "🗑️ Remove a Book":
    st.subheader("🗑️ Remove a Book")
    removing_title = st.text_input("📝 Title",key="removing_title_input")
    confirm_key = "confirm_removal"
    
    if st.button("🗑️ Remove Book",key="remove_button"):
        found = False
        for book in collection.find():
            if removing_title.lower() in book["title"].lower():
                found = True
                st.write(f"🗑️ Book Removed: {book['title']} - {book['status']}")
                result = remove_book(book["title"])
                if result:
                    st.success("✅ Book removed successfully")
                else:
                    st.error("❌ Failed to remove book")
              
                break
            elif removing_title.lower() in book["author"].lower():
                found = True
                st.write(f"🗑️ Book Removed: {book['title']} - {book['status']}")
                result = remove_book(book["title"])
                if result:
                    st.success("✅ Book removed successfully")
                else:
                    st.error("❌ Failed to remove book")
               
                break
           
        if not found:
            st.error("❓ Book not found")

elif page == "📚 View Books":
    st.subheader("📚 View Books")
    if st.button("📋 View Books",key="view_books_button"):
        with st.spinner("⏳ Loading books..."):
            books = view_books()
            if books:
                st.markdown("### 📚 Your Library")
                st.markdown("---")
                
                for book in books:
                    status_emoji = "✅" if book['status'] == "Read" else "📖"
                    
                    st.markdown(f"""
                    <div style='background-color: #1f77b4; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                        <h3 style='color: white; margin: 0;'>📕 {book['title']}</h3>
                        <p style='margin: 10px 0; color: white;'>
                            <span style='color: #f0f2f6;'>✍️ By:</span> <strong>{book['author']}</strong><br>
                            <span style='color: #f0f2f6;'>📅 Published:</span> <strong>{book['year']}</strong><br>
                            <span style='color: #f0f2f6;'>📖 Status:</span> <strong>{book['status']}</strong> {status_emoji}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📚 Your library is empty. Add some books to get started!")
   
elif page == "🔍 Search Books":
    st.subheader("🔍 Search Books")
    search_title = st.text_input("📝 Title",key="search_title_input")
    if st.button("🔍 Search Book",key="search_book_button"):
        with st.spinner("⏳ Searching for book..."):
            found = False
            for book in collection.find():
                if search_title.lower() in book["title"].lower():
                    found = True
                    status_emoji = "✅" if book['status'] == "Read" else "📖"
                    
                    st.markdown(f"""
                    <div style='background-color: #1f77b4; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                        <h3 style='color: white; margin: 0;'>📕 {book['title']}</h3>
                        <p style='margin: 10px 0; color: white;'>
                            <span style='color: #f0f2f6;'>✍️ By:</span> <strong>{book['author']}</strong><br>
                            <span style='color: #f0f2f6;'>📅 Published:</span> <strong>{book['year']}</strong><br>
                            <span style='color: #f0f2f6;'>📖 Status:</span> <strong>{book['status']}</strong> {status_emoji}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("✅ Book found")
                    break
             
                elif search_title.lower() in book["author"].lower():
                    found = True
                    status_emoji = "✅" if book['status'] == "Read" else "📖"
                    
                    st.markdown(f"""
                    <div style='background-color: #1f77b4; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                        <h3 style='color: white; margin: 0;'>📕 {book['title']}</h3>
                        <p style='margin: 10px 0; color: white;'>
                            <span style='color: #f0f2f6;'>✍️ By:</span> <strong>{book['author']}</strong><br>
                            <span style='color: #f0f2f6;'>📅 Published:</span> <strong>{book['year']}</strong><br>
                            <span style='color: #f0f2f6;'>📖 Status:</span> <strong>{book['status']}</strong> {status_emoji}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("✅ Book found")
                    break
            if not found:
                st.error("❓ Book not found")
    
elif page == "✅ Mark as Read":
    st.subheader("✅ Mark as Read")
    query = st.text_input("📝 Title",key="mark_title_input")
    if st.button("✅ Mark as Read",key="mark_button"):
        with st.spinner("⏳ Marking as read..."):
            result = mark_as_read(query)
            if result:
                st.success("✅ Book marked as read")
            else:
                st.error("❌ Failed to mark as read")

elif page == "📊 Display Statistics":
    st.subheader("📊 Display Statistics")
    if st.button("📊 Display Statistics",key="display_statistics_button"):
        with st.spinner("⏳ Displaying statistics..."):
            stats = display_statistics()
            # Display text statistics
            st.markdown("""
                ### 📊 Library Statistics
                ---
                **📚 Total Books:** {} 📚  
                **✅ Read Books:** {} ✅  
                **📖 Unread Books:** {} 📖  
                **📈 Percentage Read:** {}% 📊
            """.format(
                stats['total'],
                stats['read'], 
                stats['unread'],
                stats['percent_read']
            ))
            
            
else:
    st.write("⚠️ Invalid page")
