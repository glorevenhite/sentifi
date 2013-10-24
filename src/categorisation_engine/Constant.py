DATABASE_NAME = 'autocategory'
TABLE_RULE_CATEGORY = 'tbl_rule'
TABLE_CATEGORIES = 'tbl_category'
TABLE_FIELDS = 'tbl_applied_field'
TABLE_RULE_FIELD = 'tbl_rule_applied'
TABLE_RULE_KEYWORD = 'tbl_rule_keyword'
TABLE_KEYWORDS = 'tb_keyword'

""" Define CONSTANTs for conveniently access """
class Phases(object):
    def __init__(self):
        self.VALUES = {'PT':'PROFILE TYPE', 'PG':'PROFILE GROUP', 'C1':'CATEGORY 1', 'C2':'CATEGORY2'}

class Fields(object):
    def __init__(self):
        self.VALUES = {1:'twitter_description', 2:'twitter_screen_name', 3:'twitter_full_name'}

class Profile(object):
    def __init__(self):
        self.PER = 'PERSONAL'
        self.ORG = 'ORGANISATION'
        self.UNKNOWN = 'UNKNOWN'
        self.PROFILES = [self.PER, self.ORG]
        self.VALUES = {'P':'personal', 'O':'organization','U':'unknown'}

class Category2(object):
    def __init__(self):
        self.SELL_SIDE = 'SELL SIDE ANALYST'
        self.COMMODITY = 'COMMODITY TRADER'
        self.FOREX = 'FOREX TRADER'
        self.EQUITY = 'EQUITY TRADER'
        self.OTHER = 'TRADER OTHER'
        self.CATEGORY2 = [self.SELL_SIDE, self.COMMODITY, self.FOREX, self.EQUITY, self.OTHER]

class Category1(object):
    def __init__(self):
        self.PROFESSIONALS = 'FINANCIAL MARKET PROFESSIONALS'
        self.MARKET_STAKEHOLDERS = 'OTHER FINANCIAL MARKET STAKEHOLDER'
        self.SERVICES = 'FINANCIAL SERVICES'

        self. PUBLISHER = 'NEW PUBLISHERS'

        self.ANALYST = 'FINANCIAL ANALYST'
        self.PORTFOLIO = 'PORTFOLIO MANAGER'
        self.TRADER = 'TRADER'
        self.RISK_PROFESSIONAL = 'RISK PROFESSIONAL'
        self.CFO = 'CFO'
        self.INVESTOR_RELATIONS = 'INVESTOR RELATIONS PROFESSIONAL'
        self.OTHER_PROFESSIONAL = 'OTHER FINANCIAL PROFESSIONAL'

        self.JOURNALIST = 'JOURNALIST'

        self.BANK = 'BANK'
        self.ASSET_MANAGEMENT = 'ASSET MANAGEMENT'
        self.ADVISORY = 'FINANCIAL ADVISORY'
        self.TRADING_COM = 'TRADING COMPANY'
        self.BROKERAGE_COM = 'BROKERATE COMPANY'
        self.RESEARCH_ORG = 'FINANCIAL RESEARCH ORGANISATION'
        self.PLATFORMS = 'FINANCIAL PLATFORMS'
        self.OTHER_SERVICES = 'OTHER FINANCIAL SERVICES'
        self.DAILY_NEWS = 'DAILY NEWS'

        self.NEWS_FINANCIAL = 'NEWS FINANCIAL MARKETS'

        #self.CATEGORY = [self.PER, self.ORG, self.NEWS]

class SQLTableName(object):
    def __init__(self):
        self.DATABASE = 'autocategory'
        self.RULE_CATEGORY = 'tbl_rule'
        self.CATEGORIES = 'tbl_category'
        self.FIELDS = 'tbl_applied_field'
        self.RULES_FIELS = 'tbl_rule_applied'
        self.RULE_KEYWORD = 'tbl_rule_keyword'
        self.KEYWORDS = 'tb_keyword'

        self.KEYWORDS = 'tb_keyword'
