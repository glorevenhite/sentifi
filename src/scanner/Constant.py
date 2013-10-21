""" Define CONSTANTs for conveniently access """
class Profile(object):
    def __init__(self):
        self.PER = 'PERSONAL'
        self.ORG = 'ORGANISATION'
        self.NEWS = 'NEWS'
        self.UNKNOWN = 'UNKNOWN'
        self.PROFILE = [self.PER, self.ORG, self.NEWS]

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