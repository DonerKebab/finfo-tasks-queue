from ..core import db, es


def index_effective_secinfo():
	query = ("select s.code as symbol"
			", DECODE(s.floor_code,'10','HOSE','02','HNX','03','UPCOM') as floorcode"
			", DECODE(c.sec_type,'STOCK','ST','IFC','FC','BOND','BO','ETF','ET',c.sec_type) as type"
			", DECODE(s.floor_code,'10',s.basic_price*10,s.basic_price) as basic"
			", DECODE(s.floor_code,'10',s.ceiling_price*10,s.ceiling_price) as ceil"
			", DECODE(s.floor_code,'10',s.floor_price*10,s.floor_price) as floor"
			", DECODE(s.floor_code,'10',s.current_price*10,s.current_price) as match"
			", s.trading_status as status"
			", s.current_room*10 as currentroom"
			", s.trading_date"
			" from ipa.ifo_sec_code c, quote.sec_info s"
			" where s.trading_date = (select max(trading_date) from quote.sec_info)"
			" and c.sec_code = s.code"
			" union"
			" select d.code as symbol"
			" , DECODE(d.floor_code,'10','HOSE','DER01','HNX') as floorcode"
			", dc.derivative_type as type"
			", DECODE(d.basic_price,null,(d.ceiling_price+d.floor_price)/2,0,(d.ceiling_price+d.floor_price)/2,d.basic_price) as basic"
			", d.ceiling_price as ceil"
			", d.floor_price as floor"
			", d.current_price as match"
			", d.trading_status as status"
			", null as currentroom"
			", d.trading_date"
			" from ipa.ifo_derivative_code dc, quote.derivative_info d"
			" where d.trading_date = (select max(trading_date) from quote.derivative_info)"
			" and dc.derivative_code = d.code")

	result = db.engine.execute(query)
		
	es.publish_effective_secinfo(result, 'effective_secinfo', 'symbol')