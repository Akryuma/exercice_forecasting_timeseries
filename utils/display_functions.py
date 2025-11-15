from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def evaluate_model(y_test, y_pred, model_name="Model"):
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Linear Regression - MSE: {mse}, MAE: {mae}")

    plotly_df = pd.DataFrame({
        "Index": np.arange(len(y_test)),
        "True values": y_test,
        "Predicted": y_pred
    })
    px.line(plotly_df, x="Index", y=["True values", "Predicted"], title=f"{model_name} - True vs Predicted values (x = Time index)").show()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=plotly_df["True values"], y=plotly_df["Predicted"], mode='markers', name='True values vs. Predicted'))
    fig.add_trace(go.Scatter(x=[plotly_df["True values"].min(), plotly_df["True values"].max()],
                             y=[plotly_df["True values"].min(), plotly_df["True values"].max()],
                             mode='lines', name='y=x', line=dict(dash='dash')))
    fig.update_layout(title=f"{model_name} - True vs Predicted values scatter plot")
    
    fig.show()

