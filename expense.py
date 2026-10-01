import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from datetime import date

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f8f9ff, #eef2ff);
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #312e81;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #64748b;
        margin-bottom: 25px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0px 5px 18px rgba(0,0,0,0.08);
        border-left: 5px solid #6366f1;
    }

    div[data-testid="metric-container"] label {
        color: #64748b !important;
    }

    div[data-testid="metric-container"] div {
        color: #312e81 !important;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        border: none;
        padding: 8px 18px;
        font-weight: 600;
        background: #6366f1;
        color: white;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background: #4338ca;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #312e81, #4338ca);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Dataframe */
    .dataframe {
        border-radius: 10px;
    }

    /* Section headings */
    .section-title {
        color: #312e81;
        font-size: 25px;
        font-weight: 700;
        margin-top: 20px;
    }

    /* Info cards */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# FILE CONFIGURATION
# =========================================================

DATA_FILE = "expenses.json"


# =========================================================
# JSON FUNCTIONS
# =========================================================

def load_expenses():
    """
    Read expenses from local JSON file.
    """

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses):
    """
    Save expenses to local JSON file.
    """

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


# =========================================================
# SESSION STATE
# =========================================================

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

if "selected_expense" not in st.session_state:
    st.session_state.selected_expense = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# =========================================================
# CRUD FUNCTIONS
# =========================================================

def create_expense(expense):
    """
    CREATE operation
    """

    st.session_state.expenses.append(expense)

    save_expenses(st.session_state.expenses)


def update_expense(expense_id, updated_expense):
    """
    UPDATE operation
    """

    for index, expense in enumerate(st.session_state.expenses):

        if expense["id"] == expense_id:

            st.session_state.expenses[index] = updated_expense

            break

    save_expenses(st.session_state.expenses)


def delete_expense(expense_id):
    """
    DELETE operation
    """

    st.session_state.expenses = [
        expense
        for expense in st.session_state.expenses
        if expense["id"] != expense_id
    ]

    save_expenses(st.session_state.expenses)


def get_expense(expense_id):
    """
    READ one expense.
    """

    for expense in st.session_state.expenses:

        if expense["id"] == expense_id:
            return expense

    return None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 💰 Expense Tracker")

    st.markdown("---")

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

    if st.button("➕ Add Expense", use_container_width=True):
        st.session_state.page = "Add Expense"

    if st.button("📋 Manage Expenses", use_container_width=True):
        st.session_state.page = "Manage Expenses"

    if st.button("📊 Analytics", use_container_width=True):
        st.session_state.page = "Analytics"

    st.markdown("---")

    st.markdown("### 💾 Storage")

    st.info(
        "All expense data is stored locally in "
        "`expenses.json`."
    )

    st.markdown("---")

    st.caption("Expense Tracker • Streamlit")


# =========================================================
# DATAFRAME
# =========================================================

if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    df["amount"] = pd.to_numeric(df["amount"])

else:

    df = pd.DataFrame(
        columns=[
            "id",
            "date",
            "title",
            "category",
            "amount",
            "description"
        ]
    )


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="main-title">💰 My Expense Tracker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Track, manage and understand your spending.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    total_expenses = len(df)

    total_amount = df["amount"].sum() if not df.empty else 0

    average_expense = (
        df["amount"].mean()
        if not df.empty
        else 0
    )

    highest_expense = (
        df["amount"].max()
        if not df.empty
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💳 Total Expenses",
        total_expenses
    )

    col2.metric(
        "💰 Total Spent",
        f"₹{total_amount:,.2f}"
    )

    col3.metric(
        "📊 Average Expense",
        f"₹{average_expense:,.2f}"
    )

    col4.metric(
        "🔥 Highest Expense",
        f"₹{highest_expense:,.2f}"
    )

    st.markdown("")

    # -----------------------------------------------------
    # DASHBOARD CHARTS
    # -----------------------------------------------------

    if not df.empty:

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                '<div class="section-title">'
                '📊 Spending by Category'
                '</div>',
                unsafe_allow_html=True
            )

            category_data = (
                df.groupby("category")["amount"]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                category_data,
                names="category",
                values="amount",
                hole=0.45,
                title="Expense Distribution"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.markdown(
                '<div class="section-title">'
                '📈 Spending Trend'
                '</div>',
                unsafe_allow_html=True
            )

            trend_data = (
                df.groupby("date")["amount"]
                .sum()
                .reset_index()
            )

            trend_data["date"] = pd.to_datetime(
                trend_data["date"]
            )

            trend_data = trend_data.sort_values("date")

            fig = px.line(
                trend_data,
                x="date",
                y="amount",
                markers=True,
                title="Daily Spending"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------------------------
        # RECENT EXPENSES
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🧾 Recent Expenses'
            '</div>',
            unsafe_allow_html=True
        )

        recent = df.sort_values(
            "date",
            ascending=False
        ).head(5)

        st.dataframe(
            recent[
                [
                    "date",
                    "title",
                    "category",
                    "amount",
                    "description"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expenses available yet. "
            "Go to 'Add Expense' to create your first record."
        )


# =========================================================
# ADD EXPENSE
# =========================================================

elif st.session_state.page == "Add Expense":

    st.markdown(
        '<div class="main-title">➕ Add New Expense</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Enter the details of your expense.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("add_expense_form"):

        col1, col2 = st.columns(2)

        with col1:

            expense_date = st.date_input(
                "📅 Date",
                value=date.today()
            )

            title = st.text_input(
                "📝 Expense Title",
                placeholder="Example: Grocery Shopping"
            )

            category = st.selectbox(
                "🏷️ Category",
                [
                    "Food",
                    "Travel",
                    "Shopping",
                    "Bills",
                    "Education",
                    "Entertainment",
                    "Health",
                    "Other"
                ]
            )

        with col2:

            amount = st.number_input(
                "💰 Amount (₹)",
                min_value=0.0,
                step=10.0,
                format="%.2f"
            )

            description = st.text_area(
                "📄 Description",
                placeholder="Add a short description..."
            )

        submitted = st.form_submit_button(
            "💾 Save Expense",
            use_container_width=True
        )

        if submitted:

            if not title.strip():

                st.error("Please enter an expense title.")

            elif amount <= 0:

                st.error("Amount must be greater than ₹0.")

            else:

                new_id = (
                    max(
                        [
                            expense["id"]
                            for expense in st.session_state.expenses
                        ],
                        default=0
                    )
                    + 1
                )

                new_expense = {
                    "id": new_id,
                    "date": str(expense_date),
                    "title": title.strip(),
                    "category": category,
                    "amount": amount,
                    "description": description.strip()
                }

                create_expense(new_expense)

                st.success(
                    "Expense added successfully!"
                )

                st.session_state.page = "Manage Expenses"

                st.rerun()


# =========================================================
# MANAGE EXPENSES
# =========================================================

elif st.session_state.page == "Manage Expenses":

    st.markdown(
        '<div class="main-title">📋 Manage Expenses</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View, edit and delete your expense records.'
        '</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.info(
            "No expenses found. Add an expense first."
        )

    else:

        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        search = st.text_input(
            "🔍 Search expenses",
            placeholder="Search by title or category..."
        )

        filtered_df = df.copy()

        if search:

            filtered_df = filtered_df[
                filtered_df["title"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                filtered_df["category"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            filtered_df[
                [
                    "id",
                    "date",
                    "title",
                    "category",
                    "amount",
                    "description"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # -------------------------------------------------
        # SELECT EXPENSE
        # -------------------------------------------------

        expense_ids = filtered_df["id"].tolist()

        if expense_ids:

            selected_id = st.selectbox(
                "Select an expense to modify",
                expense_ids
            )

            selected = get_expense(
                selected_id
            )

            col1, col2 = st.columns(2)

            # -------------------------------------------------
            # UPDATE
            # -------------------------------------------------

            with col1:

                st.markdown(
                    "### ✏️ Update Expense"
                )

                with st.form("update_form"):

                    updated_date = st.date_input(
                        "Date",
                        value=pd.to_datetime(
                            selected["date"]
                        ).date()
                    )

                    updated_title = st.text_input(
                        "Title",
                        value=selected["title"]
                    )

                    categories = [
                        "Food",
                        "Travel",
                        "Shopping",
                        "Bills",
                        "Education",
                        "Entertainment",
                        "Health",
                        "Other"
                    ]

                    current_category = (
                        selected["category"]
                        if selected["category"] in categories
                        else "Other"
                    )

                    updated_category = st.selectbox(
                        "Category",
                        categories,
                        index=categories.index(
                            current_category
                        )
                    )

                    updated_amount = st.number_input(
                        "Amount",
                        min_value=0.0,
                        value=float(
                            selected["amount"]
                        ),
                        step=10.0
                    )

                    updated_description = st.text_area(
                        "Description",
                        value=selected["description"]
                    )

                    update_button = st.form_submit_button(
                        "💾 Update Expense",
                        use_container_width=True
                    )

                    if update_button:

                        updated_expense = {
                            "id": selected["id"],
                            "date": str(updated_date),
                            "title": updated_title,
                            "category": updated_category,
                            "amount": updated_amount,
                            "description": updated_description
                        }

                        update_expense(
                            selected["id"],
                            updated_expense
                        )

                        st.success(
                            "Expense updated successfully!"
                        )

                        st.rerun()

            # -------------------------------------------------
            # DELETE
            # -------------------------------------------------

            with col2:

                st.markdown(
                    "### 🗑️ Delete Expense"
                )

                st.warning(
                    f"You selected: **{selected['title']}**"
                )

                st.write(
                    f"Amount: ₹{selected['amount']:,.2f}"
                )

                st.write(
                    f"Category: {selected['category']}"
                )

                st.write(
                    "Deleting this expense will permanently "
                    "remove it from the JSON file."
                )

                confirm_delete = st.checkbox(
                    "I understand that this cannot be undone."
                )

                if st.button(
                    "🗑️ Delete Expense",
                    use_container_width=True
                ):

                    if confirm_delete:

                        delete_expense(
                            selected["id"]
                        )

                        st.success(
                            "Expense deleted successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Please confirm deletion first."
                        )


# =========================================================
# ANALYTICS
# =========================================================

elif st.session_state.page == "Analytics":

    st.markdown(
        '<div class="main-title">📊 Expense Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Understand where your money is going.'
        '</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.info(
            "Add some expenses to see analytics."
        )

    else:

        # -------------------------------------------------
        # CATEGORY ANALYSIS
        # -------------------------------------------------

        category_data = (
            df.groupby("category")["amount"]
            .sum()
            .reset_index()
            .sort_values(
                "amount",
                ascending=False
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                category_data,
                x="category",
                y="amount",
                title="💰 Expense by Category",
                text_auto=".2f"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            fig = px.pie(
                category_data,
                names="category",
                values="amount",
                hole=0.5,
                title="🥧 Category Distribution"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------------------------
        # MONTHLY ANALYSIS
        # -------------------------------------------------

        analytics_df = df.copy()

        analytics_df["date"] = pd.to_datetime(
            analytics_df["date"]
        )

        analytics_df["month"] = (
            analytics_df["date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_data = (
            analytics_df
            .groupby("month")["amount"]
            .sum()
            .reset_index()
        )

        st.markdown(
            "### 📅 Monthly Spending"
        )

        fig = px.line(
            monthly_data,
            x="month",
            y="amount",
            markers=True,
            title="Monthly Expense Trend"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -------------------------------------------------
        # TOP EXPENSES
        # -------------------------------------------------

        st.markdown(
            "### 🔥 Highest Expenses"
        )

        top_expenses = (
            df.sort_values(
                "amount",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            top_expenses,
            x="title",
            y="amount",
            color="category",
            title="Top 10 Expenses",
            text_auto=".2f"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        st.markdown(
            "### 📈 Spending Statistics"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Minimum Expense",
            f"₹{df['amount'].min():,.2f}"
        )

        col2.metric(
            "Maximum Expense",
            f"₹{df['amount'].max():,.2f}"
        )

        col3.metric(
            "Total Spending",
            f"₹{df['amount'].sum():,.2f}"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b;">
        💰 <b>Expense Tracker</b> |
        Built with Python + Streamlit |
        Data stored locally using JSON
    </div>
    """,
    unsafe_allow_html=True
)