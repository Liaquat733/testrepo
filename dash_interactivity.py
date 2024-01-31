{
  "metadata": {
    "kernelspec": {
      "name": "xeus-python",
      "display_name": "Python (XPython)",
      "language": "python"
    },
    "language_info": {
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "version": "3.10.2"
    }
  },
  "nbformat_minor": 4,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "Hands-on Lab: Build an Interactive Dashboard with Ploty Dash",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "code",
      "source": "!pip install dash\n!pip install dash==1.19.0\n!pip install jupyter_dash\n!pip install --upgrade plotly",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "code",
      "source": "from jupyter_dash.comms import _send_jupyter_config_comm_request\n_send_jupyter_config_comm_request()",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "code",
      "source": "import pandas as pd\nimport dash\nimport dash_html_components as html\nimport dash_core_components as dcc\nfrom dash.dependencies import Input, Output\nfrom jupyter_dash import JupyterDash\nimport plotly.graph_objects as go",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "code",
      "source": "# notebook hangs if I run the following command \nJupyterDash.infer_jupyter_proxy_config()",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "code",
      "source": "# needs to be run again in a separate cell due to a jupyterdash bug\nJupyterDash.infer_jupyter_proxy_config()",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "code",
      "source": "wget \"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv\"",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "code",
      "source": "# Import required libraries\n# import pandas as pd\n# import dash\n# import dash_html_components as html\n# import dash_core_components as dcc\n# from dash.dependencies import Input, Output\nimport plotly.express as px\n\n# Read the airline data into pandas dataframe\n# spacex_df = pd.read_csv(\"spacex_launch_dash.csv\")\nmax_payload = spacex_df['Payload Mass (kg)'].max()\nmin_payload = spacex_df['Payload Mass (kg)'].min()\n\n# Create a dash application\n# app = dash.Dash(__name__) # commented out as we are using JupyterDash instead of dash.Dash\napp = JupyterDash(__name__)\n\n# Create an app layout\napp.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',\n                                        style={'textAlign': 'center', 'color': '#503D36',\n                                               'font-size': 40}),\n                                # TASK 1: Add a dropdown list to enable Launch Site selection\n                                # The default select value is for ALL sites\n                                # dcc.Dropdown(id='site-dropdown',...)\n                                dcc.Dropdown(id='site-dropdown',\n                                             options=[\n                                                     {'label': 'All Sites', 'value': 'ALL'},\n                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},\n                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},\n                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},\n                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}\n                                                     ],\n                                             value='ALL',\n                                             placeholder='Select a Launch Site here',\n                                             searchable=True\n                                             # style={'width':'80%','padding':'3px','font-size':'20px','text-align-last':'center'}\n                                             ),\n                                html.Br(),\n\n                                # TASK 2: Add a pie chart to show the total successful launches count for all sites\n                                # If a specific launch site was selected, show the Success vs. Failed counts for the site\n                                html.Div(dcc.Graph(id='success-pie-chart')),\n                                html.Br(),\n\n                                html.P(\"Payload range (Kg):\"),\n                                # TASK 3: Add a slider to select payload range\n                                #dcc.RangeSlider(id='payload-slider',...)\n                                dcc.RangeSlider(id='payload-slider',\n                                                min=0,\n                                                max=10000,\n                                                step=1000,\n                                                value=[min_payload, max_payload]\n                                                ),\n\n                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success\n                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),\n                                ])\n\n# TASK 2:\n# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output\n@app.callback(Output(component_id='success-pie-chart', component_property='figure'),\n              Input(component_id='site-dropdown', component_property='value'))\ndef get_pie_chart(entered_site):\n    filtered_df = spacex_df\n    if entered_site == 'ALL':\n        fig = px.pie(filtered_df, values='class', \n        names='Launch Site', \n        title='Success Count for all launch sites')\n        return fig\n    else:\n        # return the outcomes piechart for a selected site\n        filtered_df=spacex_df[spacex_df['Launch Site']== entered_site]\n        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')\n        fig=px.pie(filtered_df,values='class count',names='class',title=f\"Total Success Launches for site {entered_site}\")\n        return fig\n\n# TASK 4:\n# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output\n@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),\n                [Input(component_id='site-dropdown',component_property='value'),\n                Input(component_id='payload-slider',component_property='value')])\ndef scatter(entered_site,payload):\n    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]\n    # thought reusing filtered_df may cause issues, but tried it out of curiosity and it seems to be working fine\n    \n    if entered_site=='ALL':\n        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')\n        return fig\n    else:\n        fig=px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f\"Success count on Payload mass for site {entered_site}\")\n        return fig\n\n#\n\n Run the app\nif __name__ == '__main__':\n    app.run_server(mode='inline', host='localhost')\n\n",
      "metadata": {
        "trusted": true
      },
      "outputs": [],
      "execution_count": null
    }
  ]
}