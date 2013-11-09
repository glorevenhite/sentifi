TWITTER = "Twitter"
TWITTER_SCREEN_NAME = "Twitter Screen Name"
TWITTER_FULL_NAME = "Twitter Name"
TWITTER_DESCRIPTION = "Twitter Description"

FIELD_TWITTER_DESCRIPTION_ID = '76'
FIELD_TWITTER_SCREEN_NAME_ID = '2'
FIELD_TWITTER_FULL_NAME_ID = '3'

PHASE_VALUES = ['PROFILE TYPE', 'PUBLISHER GROUP', 'CATEGORY 1', 'CATEGORY 2']

SERVER_STATUS_OK = 'OK'
SERVER_STATUS_ERROR = "ERROR"

DATABASE_NAME = 'autocategory_db'
#DATABASE_NAME = 'primitive_category_db'
TABLE_PROFILES = 'test2'

PERSONAL = "P"
P_PUBLISHER_GROUP = ['Financial Market Professionals', 'Other Stakeholders']

ORGANISATION = "O"
O_PUBLISHER_GROUP = ['Financial Services',
                     'News Publishers',
                     'Technology Market Participants',
                     'Other Companies',
                     'Education Organisations',
                     'Government Organisations',
                     'Non-Governmental Organisations',
                     'Non identified Stakeholder',
                     'Undefined']
END_POINT_URL = 'http://categories.sentifi.com/index.php/api/'
END_POINT_KEY = '&authkey=4YJEe6zcPYAkBwFV8Nae'

GET_CATEGORY_BY_ID = END_POINT_URL + 'getCategoryKeywordById?id={0}&' + END_POINT_KEY

CAT1_PARENT = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 44]

CAT2_PARENT_ID = [45, 46, 47, 55, 61, 64, 68, 89, 87, 93, 179]

CAT2_PARENT = ['Buy Side Analyst',
               'Sell Side Analyst',
               'Other',
               'Activist Investor',
               'Commodity Trader',
               'Currency Trader',
               'Trader - Other',
               'Equity - Trader',
               'Fixed Income Trader',
               'Volatility Trader',
               'Credit Trader',
               'Multi-Asset-Class Trader',
               'Financial Planner',
               'Business and Financial Journalist',
               'Technology Analyst',
               'Journalist - Other',
               'Central bank',
               'Bank - other',
               'Brokerage Company',
               'Prop. Trading Company',
               'Trading platforms (incl. Signals)',
               'Investor Networks',
               'National News',
               'Local News',
               'Other News',
               'Business']


