from ..core import db, es


def index_effective_secinfo():
	query = ("select code as symbol"
				", DECODE(floor_code,'10','HOSE','02','HNX','03','UPCOM') as floorcode"
				", sec_type as type"
				", DECODE(floor_code,'10',basic_price*10,basic_price) as basic"
				", DECODE(floor_code,'10',ceiling_price*10,ceiling_price) as ceil"
				", DECODE(floor_code,'10',floor_price*10,floor_price) as floor"
				", DECODE(floor_code,'10',current_price*10,current_price) as match"
				", trading_status as status"
				", current_room*10 as currentroom"
				", trading_date"
				" from ifo_sec_code c, quote.sec_info s"
				" where trading_date = (select max(trading_date) from quote.sec_info)"
				" and c.sec_code = s.code"
				" and c.sec_type not in ('BOND')"
				" union"
				" select code as symbol"
				", DECODE(floor_code,'10','HOSE','DER01','HNX') as floorcode"
				", derivative_type as type"
				", DECODE(basic_price,null,(ceiling_price+floor_price)/2,0,(ceiling_price+floor_price)/2,basic_price) as basic"
				", ceiling_price as ceil"
				", floor_price as floor"
				", current_price as match"
				", trading_status as status"
				", null as currentroom"
				", trading_date"
				" from ifo_derivative_code c, quote.derivative_info s"
				" where trading_date = (select max(trading_date) from quote.derivative_info)"
				" and c.derivative_code = s.code")

	result = db.engine.execute(query)
		
	es.publish(result, 'effective_secinfo', 'symbol')