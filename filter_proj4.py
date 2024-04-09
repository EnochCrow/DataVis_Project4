import pandas as pd
from io import StringIO
import json

# Input file path
orig_file_path = 'COW_Trade_4.0\\Dyadic_COW_4.0.csv'

# temp Output file path
temp_file_path = 'ww2_year_import_export_total.csv'

# Read data from input file path
ww2_trade_df = pd.read_csv(orig_file_path)
columns_to_keep = ['year','importer1','importer2','flow1','flow2']
ww2_trade_df = ww2_trade_df[columns_to_keep]
ww2_trade_df = ww2_trade_df[ww2_trade_df['flow1'] != -9]
ww2_trade_df = ww2_trade_df[ww2_trade_df['flow2'] != -9]
ww2_trade_df = ww2_trade_df.reset_index(drop=True)
ww2_trade_df.to_csv(temp_file_path)

def filter_data(in_filepath, chosen_year):
    # Read the CSV data into a string
    # print(in_filepath)
    
    # Read CSV-formatted text file into a pandas DataFrame, specifying the header row
    df = pd.read_csv(in_filepath)

    filtered_df = df[df['year'] == chosen_year]
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df = filtered_df.drop(columns='Unnamed: 0')

    out_name = "Formatted_Data\\ww2_trade_" + str(chosen_year) + ".csv"
    filtered_df.to_csv(out_name)


    final_out = "Final_Data\\ww2_network_" + str(chosen_year) + ".csv"

    filtered_df = filtered_df.drop(columns='year')

    col1 = 'source'
    col2 = 'target'
    col3 = 'value'
    new_df = pd.DataFrame(columns=[col1,col2,col3])
    for i in range(len(filtered_df)):
        row1 = {}
        row2 = {}
        row1[col1] = filtered_df.loc[i, 'importer2']
        row1[col2] = filtered_df.loc[i, 'importer1']
        row1[col3] = filtered_df.loc[i, 'flow1']

        row2[col1] = filtered_df.loc[i, 'importer1']
        row2[col2] = filtered_df.loc[i, 'importer2']
        row2[col3] = filtered_df.loc[i, 'flow2']

        row1_df = pd.DataFrame(row1, index=[0])
        row2_df = pd.DataFrame(row2, index=[0])
        
        new_df = pd.concat([new_df, row1_df], ignore_index=True)
        new_df = pd.concat([new_df, row2_df], ignore_index=True)

    new_df['source'] = new_df['source'].replace('United States of America', 'United States')
    new_df['target'] = new_df['target'].replace('United States of America', 'United States')
    # source_nations = ['United States of America']
    # dest_nations = ['Germany', 'Japan']
    new_df = new_df.drop_duplicates()
    new_df.to_csv(final_out)

    # new_df_test = new_df[new_df['source'].isin(source_nations)]
    # new_df_test = new_df_test[new_df_test['target'].isin(dest_nations)]
    # new_df_test['year'] = chosen_year
    #print(new_df_test.head())


    links_json = {"links": new_df.to_dict(orient="records")}
    # print(type(links_json))
    #print(links)
    links = links_json["links"]
    #print(links)

    # Convert JSON data to a string
    json_str = json.dumps(links, indent=4)
    #print(json_str)

    # Extract unique node IDs from source and target
    node_ids = set()
    for link in links:
        node_ids.add(link["source"])
        node_ids.add(link["target"])

    axis = ['Germany','Italy','Japan','Hungary','Romania','Bulgaria','Finland','Croatia','Thailand']
    allies = ['United Kingdom','United States','Russia','France','Poland','Belgium','Luxembourg','Netherlands','Norway','Greece','Yugoslavia','Ethiopia','Phillipines','China','Canada','Australia','New Zealand','South Africa','Brazil','Mexico','Mongolia']

    # Create nodes list

    nodes = [{"id": node_id, "group": 1 if node_id in allies else (2 if node_id in axis else 3)} for node_id in node_ids]

    # Create JSON object
    nodes_json = {"nodes": nodes}

    def remove_group(nodes, links, group_to_remove):
        # Filter out nodes with the specified group value
        filtered_nodes = [node for node in nodes if node["group"] != group_to_remove]
        
        # Filter out links where both source and target nodes belong to the specified group value
        filtered_links = [link for link in links 
                        if (link["source"] in [node["id"] for node in filtered_nodes])
                        and (link["target"] in [node["id"] for node in filtered_nodes])]
        
        return filtered_nodes, filtered_links

    # Specify the group value to remove
    group_to_remove = 3

    # Remove nodes and links of the specified group value
    filtered_nodes, filtered_links = remove_group(nodes, links, group_to_remove)
    nodes_json = {"nodes": filtered_nodes}
    links_json = {"links": filtered_links}

    # Convert to JSON string
    json_str = json.dumps(nodes_json, indent=4)

    # Print JSON string
    #print(json_str)

    combined_data = {}
    combined_data["nodes"] = nodes_json["nodes"]
    combined_data["links"] = links_json["links"]

    out_json = "final_jsons\\ww2_trade_" + str(chosen_year) + ".json"

    with open(out_json, "w") as json_file:
        json.dump(combined_data, json_file, indent=4)

    print("Final JSON exported to",out_json)

us_export_data = pd.DataFrame()
for i in range(1939, 1945):
    filter_data(temp_file_path, i)

#us_export_data.to_csv('us_export_data_ww2.csv')
