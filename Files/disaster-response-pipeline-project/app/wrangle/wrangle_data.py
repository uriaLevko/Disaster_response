import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
# TODO: Scroll down to line 157 and set up a fifth visualization for the data dashboard
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('data/DisasterResponse.db', engine)
# print(df.columns,df.shape)
def cleandata(df):
    """Clean world bank data for a visualizaiton dashboard

    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """   
    # Keep only the columns of interest
#     print(df)
    df_rel = df.iloc[:,4:]
    
    # if any feature higher then 1 fix it
    for col in df_rel.columns:
        df_rel[col] = df_rel[col].apply(lambda x:1 if x>1 else x)

        
    return df_rel

def fix_features(df):
    safe_spots = ['offer','shelter']
    facilities = ['hospitals','aid_centers','other_infrastructure','buildings','infrastructure_related','shops','shelter']
    needs = ['clothing','electricity','money','transport','medical_products','water','medical_help','tools','shelter','food','refugees']
    conditions = ['cold','other_weather','floods','fire','storm','earthquake']
    medical = ['medical_products','medical_help','hospitals']
    search_and_rescue = ['search_and_rescue','missing_people','request','death']
    security =['security','military']
    columns = [safe_spots,facilities,needs,conditions,medical,search_and_rescue,security]
    columnName = ['safe_spots','facilities','needs','conditions','medical','search_and_rescue','security']
    
    for i,col in enumerate(columns):
        df[columnName[i]] = df[col].sum(axis=1)#sum features on columns
        
    divisionDF = df.mean()
    divDF = divisionDF[(divisionDF<.7) & (divisionDF>.03)]#keep only relavant columns
    return divDF


def return_figures(df):
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

  # first chart plots arable land from 1990 to 2015 in top 10 economies 
  # as a line chart
    
    graph_one = []
    dfC = cleandata(df)
    dfC = dfC.mean()
    dfc = dfC.sort_values()
#     dfc['status']=dfc.apply(lambda x:'bad' if (x<0.3 or x>0.7) else 'good')
#     colors = {'good':'steelblue',
#           'bad':'firebrick'}
    graph_one.append(
        go.Bar(
        x = dfC.index,
        y = dfC,marker={'color':dfC,'colorscale': 'inferno'}
            
    #           mode = 'lines'

          )
      )

    layout_one = dict(title = 'Feature Unbalance review in Dataset',
                xaxis = dict(title = 'Classes',
                  autotick=True,tickangle=45,
                            categoryorder="max ascending"),
                yaxis = dict(title = 'Ratio of accurence labeled as 1'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    
    graph_two = []
    df_two = cleandata(df)
    df_two_fix = fix_features(df_two)
    df_two_fix.sort_values()
    
    graph_two.append(
      go.Bar(
      x = df_two_fix.index,
      y = df_two_fix,marker={'color':df_two_fix,'colorscale': 'inferno'}
      )
    )

    layout_two = dict(title = 'Feature Unbalance review in Dataset - after correction',
                xaxis = dict(title = 'Classes',categoryorder="max ascending"),
                yaxis = dict(title = 'Ratio of accurence labeled as 1'))
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    

    return figures