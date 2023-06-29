import streamlit as st

# CSS styling
css = """
<style>
h1 {
    color: #0066CC;
    font-size: 28px;
    margin-top: 30px;
    margin-bottom: 20px;
}

h2 {
    color: #0099FF;
    font-size: 22px;
    margin-top: 25px;
    margin-bottom: 15px;
}

h3 {
    color: #00BBFF;
    font-size: 18px;
    margin-top: 20px;
    margin-bottom: 10px;
}

p {
    font-size: 16px;
    margin-bottom: 15px;
}

.code {
    background-color: #F5F5F5;
    padding: 10px;
    border-radius: 5px;
}

</style>
"""

# Streamlit app setup
def app():
    # Add CSS styling
    with open("doc.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Introduction section
    st.markdown("<h1>Documentation</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Introduction</h2>", unsafe_allow_html=True)
    st.markdown("<p>Welcome to the documentation for Cleo, a powerful and versatile chat and voice assistant. Cleo is designed to assist you with various tasks, from running MySQL queries to managing your to-do lists, setting reminders, opening apps, browsing the internet for videos, songs, and information, utilizing AI and NLP with OpenAI's APIs, generating images, performing speed tests, and more.</p>", unsafe_allow_html=True)
    st.markdown("<p>This comprehensive guide will walk you through the features and functionalities of Cleo.</p>", unsafe_allow_html=True)
    
    # MySQL Queries
    with st.expander("MySQL Queries"):
        st.markdown("<p>Cleo allows you to run MySQL queries and interact with databases seamlessly. Simply provide the necessary credentials and execute your SQL queries using Cleo's intuitive interface.</p>", unsafe_allow_html=True)
        # Add image for MySQL queries
        st.image("hl.jpg", use_column_width=True)

    # To-Do Lists
    with st.expander("To-Do Lists"):
        st.markdown("<p>Cleo helps you manage your tasks efficiently with its built-in to-do list feature. Add, update, and remove tasks easily, and mark them as completed when you're done.</p>", unsafe_allow_html=True)
        # Add image for to-do lists
        st.image("hl.jpg", use_column_width=True)

    # Reminders
    with st.expander("Reminders"):
        st.markdown("<p>Never forget important events or deadlines again! Cleo enables you to set reminders for various tasks and events. Cleo will notify you at the specified time to ensure you stay on top of your schedule.</p>", unsafe_allow_html=True)
        # Add image for reminders
        st.image("hl.jpg", use_column_width=True)

    # Open Apps
    with st.expander("Open Apps"):
        st.markdown("<p>Cleo can help you launch applications on your system quickly. Just provide the name or path of the app, and Cleo will open it for you.</p>", unsafe_allow_html=True)
        # Add image for opening apps
        st.image("hl.jpg", use_column_width=True)

    # Internet Browsing
    with st.expander("Internet Browsing"):
        st.markdown("<p>Cleo can surf the internet for videos, songs, and information. You can ask Cleo to search for specific topics, play videos or songs, and retrieve valuable information from the web.</p>", unsafe_allow_html=True)
        # Add image for internet browsing
        st.image("hl.jpg", use_column_width=True)

    # AI and NLP
    with st.expander("AI and NLP"):
        st.markdown("<p>Cleo leverages AI and NLP capabilities through OpenAI's APIs. This allows Cleo to understand natural language queries, perform sentiment analysis, and generate responses that cater to your specific needs.</p>", unsafe_allow_html=True)
        # Add image for AI and NLP
        st.image("hl.jpg", use_column_width=True)

    # Image Generation
    with st.expander("Image Generation"):
        st.markdown("<p>Cleo can generate images based on various parameters and inputs. Whether you need custom graphics, charts, or visual representations, Cleo has got you covered.</p>", unsafe_allow_html=True)
        # Add image for image generation
        st.image("hl.jpg", use_column_width=True)

    # Timers
    with st.expander("Timers"):
        st.markdown("<p>Cleo can help you set up timers for different purposes. Whether it's timing your workouts, cooking, or other activities, Cleo will notify you when the time is up.</p>", unsafe_allow_html=True)
        # Add image for timers
        st.image("hl.jpg", use_column_width=True)

    # Speed Tests
    with st.expander("Speed Tests"):
        st.markdown("<p>Cleo can perform speed tests to measure your network's upload and download speeds. It helps you monitor your internet connection and identify any potential issues.</p>", unsafe_allow_html=True)
        # Add image for speed tests
        st.image("hl.jpg", use_column_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    app()
