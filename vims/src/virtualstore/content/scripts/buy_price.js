function showBuyPricePopup(){

	var html = null;
	var bp_json = $("#id_buy_price").val();

	if( bp_json == null || bp_json == ''){
		// empty buy price
		html = getBuyPricePopupHTML(null);
	}else{
		html = getBuyPricePopupHTML(JSON.parse(bp_json));
	}

	if( html != null){
		$.alerts.okButton = "Submit";
		jEmpty(html, "Buy Price", function(result){ if(result){ makeBuyPriceJSONFromHtmlToField(); }});
	}	
}	

function getBuyPricePopupHTML(bp_object){

	var bp_html = "<div id='main_bp_div' style='overflow:auto;max-height:20em;white-space: nowrap;'>";
		
	if( bp_object == null ){
		// empty list
		bp_html += buyPriceHtmlForValues(0, 0, null, null);
		bp_html += "</div>"
		$("#bp_index").val(1);
	}else{
		var index = 0;
		for(i in bp_object){
			index = i;
			bp_html += buyPriceHtmlForValues(i, bp_object[i]["price"], bp_object[i]["currency"], bp_object[i]["campaign"]);
		}
		bp_html += "</div>";
		index = parseInt(index) + 1;
		$("#bp_index").val(index);
	}
	return bp_html;
}

function buyPriceHtmlForValues(bp_row_id, price, currency, campaign){
	var bp_html =  "<div id='bp_"+bp_row_id+"'>"
	 	+"<input type='button' onclick='addBuyPrice()' value='+' style='font-size:1.5em;color:#00FF00' />"
	 	+"<input type='button' onclick='removeBuyPrice("+bp_row_id+")' value='-' style='font-size:1.5em;color:#FF0000' />"
	 	+"<label style='font-weight:bold;font-size:1.1em'>Price :&nbsp;</label>"
	 	+"<input type='text' maxlength='10' size='11' id='bp_price' value='"+price+"'/>&nbsp;"
	 	+"<label style='font-weight:bold;font-size:1.1em'>Currency :&nbsp;</label>"
	 	+"<select id='bp_currency'>";
		for(var idx in currency_list){
			if(currency_list[idx] == currency){
				bp_html += "<option selected value='"+currency_list[idx]+"'>"+currency_list[idx]+"</option>";
			}else{
				bp_html += "<option value='"+currency_list[idx]+"'>"+currency_list[idx]+"</option>";
			}
		}
		
		bp_html +=  "</select>&nbsp;"
				+"<label style='font-weight:bold;font-size:1.1em'>Campaign :&nbsp;</label>"
			 	+"<select id='bp_campaign'><option value='default'>default</option></select>"
			 	+"</div>"
	return bp_html;			 	
}

function addBuyPrice(){
		var index = $("#bp_index").val();
		var bp_html = buyPriceHtmlForValues(index, 0, null, null);
		$("#main_bp_div").append(bp_html);
		index = parseInt(index) + 1;
		$("#bp_index").val(index);	
}

function removeBuyPrice(index){
	$("#bp_"+index).remove();
}

function makeBuyPriceJSONFromHtmlToField(){

	var bp_list = [];
	var index = parseInt($("#bp_index").val());
	for(i=0; i < index;i++){
		if( $("#bp_"+i).length == 0 ){
			continue;
		}
		var bp_row_div = $("#bp_"+i); 
		
		var bp_data = {};
		bp_data["price"] = parseFloat(bp_row_div.find("#bp_price").val());
		bp_data["currency"] = bp_row_div.find("#bp_currency").val();
		bp_data["campaign"] = bp_row_div.find("#bp_campaign").val();

		bp_list.push(bp_data);
	}
	if(bp_list.length == 0){
		$("#id_buy_price").val("");
	}else{
		$("#id_buy_price").val(JSON.stringify(bp_list));
	}
}