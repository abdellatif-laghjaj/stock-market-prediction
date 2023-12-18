import streamlit as st

def custom_card(title, content, color="#f0f0f0"):
    """
    Create a custom card-like container.

    Parameters:
        - title (str): Title for the card.
        - content (str): Content or text to be displayed in the card.
        - color (str): Background color of the card.

    Returns:
        - None
    """
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 16px;
            border-radius: 10px;
            border: 1px solid #d4d4d4;
            background-color: {color};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 8px;
        ">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )