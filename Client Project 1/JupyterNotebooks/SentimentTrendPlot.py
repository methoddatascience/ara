
# coding: utf-8

# In[ ]:


def plot_sentiment_trends(df,term='',style='fivethirtyeight'):
    
    '''
    Takes in a dataframe, creates 2 plots, and returns a grouped dataframe (by year)
    
    Arguments:
    df - dataframe
    term - search term, usually disease name. Must be included in the disease column in the dataframe
    style - plot style, default is fivethirtyeight
    
    The 2 plots shown are:
    1) Percentage of positive articles over time 
    2) Average Article Sentiment over time
    
    The dataframed returned is grouped by year, 
    and includes the following columns for all positive articles ("_pos"), 
    negative articles("_neg") and all articles for the search term (no suffix):
    - group_date : year
    - min
    - max
    - mean
    - count
    - perc_pos -  % papers that had a positive sentiment
    
    '''
    
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    if term == '':
        raise ValueError("Must include a term using the 'term' parameter.")
    else:
        disease = term
        
    if df.empty:
        raise ValueError("Must specify a dataset using the df paramter.")
    else:

        diseases = list(df['disease'].unique())

        if str(disease).lower() in diseases:

            plt.style.use(style)

            plot_df_pos = df[(df['disease']== disease) & (df['abs_scores'] >= 0)][['abs_scores','Clean_Date']]
            plot_df_neg = df[(df['disease']== disease) & (df['abs_scores'] < 0)][['abs_scores','Clean_Date']]
            plot_df_all = df[(df['disease']== disease)][['abs_scores','Clean_Date']]


            plot_df_pos['group_date'] = plot_df_pos['Clean_Date'].apply(str).apply(lambda x: x.split('-')[0])
            plot_df_neg['group_date'] = plot_df_neg['Clean_Date'].apply(str).apply(lambda x: x.split('-')[0])
            plot_df_all['group_date'] = plot_df_all['Clean_Date'].apply(str).apply(lambda x: x.split('-')[0])



            yearly_pos = pd.DataFrame(plot_df_pos.groupby(['group_date'],
                                                          group_keys=False)['abs_scores'] \
                                                          .agg(['min','max','mean','count']))
            yearly_neg = pd.DataFrame(plot_df_neg.groupby(['group_date'],
                                                          group_keys=False)['abs_scores'] \
                                                          .agg(['min','max','mean','count']))

            yearly_all = pd.DataFrame(plot_df_all.groupby(['group_date'],
                                                          group_keys=False)['abs_scores'] \
                                                          .agg(['min','max','mean','count']))



            yearly = pd.merge(left=yearly_pos.reset_index(),
                              right=yearly_neg.reset_index(),
                              on='group_date',how='outer',
                             suffixes=['_pos','_neg'])
            yearly['perc_pos'] = yearly['count_pos'] / (yearly['count_pos'] + yearly['count_neg'])
            yearly['perc_pos'].fillna(1.0,inplace=True)

            yearly = pd.merge(left=yearly.reset_index(),
                              right=yearly_all.reset_index(),
                              on='group_date',how='outer',
                             suffixes=['','_all'])

            #print(yearly.head())
            yearly = yearly[yearly['count'] > 10].reset_index(drop=True).sort_values(by=['group_date'],ascending=True)

            n_years = yearly['group_date'].nunique()
            zeros = [0]*n_years
                                
            plt.figure(figsize=(12,6))
            plt.ylim(0,1.0)
            plt.title("Percent Positive {} Articles".format(disease))
            plt.ylabel("% Articles Positive")
            plt.plot(zeros,'--',linewidth=1,color='red')
            #yearly_pos['max'].plot(label='Max')
            #yearly_pos['min'].plot(label='Min')
            #yearly_pos['mean'].plot(label='Avg')
            plt.plot(yearly['group_date'],yearly['perc_pos'],label='Percent Positive Articles',color='DodgerBlue')
            #yearly_neg['count'].plot(label='Negative')
            plt.xlabel("Year")
            #plt.xticks(yearly.index)
            #ax.set_xticklabels(yearly['group_date'])
            plt.xticks(np.arange(len(zeros)),yearly['group_date'])
            plt.legend()

            #n_years = yearly['group_date'].nunique()
            #zeros = [0]*n_years

            plt.figure(figsize=(12,6))
            plt.title("Average {} Article Sentiment".format(disease))
            plt.ylabel("Average Total Sentiment")
            plt.plot(zeros,'--',linewidth=1,color='red')
            plt.plot(yearly['group_date'], yearly['mean'],label='Mean',color='SeaGreen')
            #yearly_neg['min'].plot(label='Min')
            #yearly_neg['mean'].plot(label='Avg')
            #yearly_neg['count'].plot(label='Count')

            plt.xlabel("Year")
            plt.xticks(yearly.index)
            plt.xticks(np.arange(len(zeros)),yearly['group_date'])
            plt.legend()
            #plt.ylim(-1,3)
            
            return yearly
        else:
            raise ValueError("Please include a valid disease. Options include: {}".format(diseases))
        

