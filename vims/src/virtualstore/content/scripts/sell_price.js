function showSellPricePopup(){

	var html = null;
	var sp_json = $("#id_sell_price").val();

	if( sp_json == null || sp_json == ''){
		// empty sell price
		html = getSellPricePopupHTML(null);
	}else{
		html = getSellPricePopupHTML(JSON.parse(sp_json));
	}

	if( html != null){
		$.alerts.okButton = "Submit";
		jEmpty(html, "Sell Price", function(result){ if(result){ makeSellPriceJSONFromHtmlToField(); }});
	}	
}	

function getSellPricePopupHTML(sp_object){

	var sp_html = "<div id='main_sp_div' style='overflow:auto;max-height:20em;white-space: nowrap;'>";
		
	if( sp_object == null ){
		// empty list
		sp_html += sellPriceHtmlForValues(0, 0, null, null);
		sp_html += "</div>"
		$("#sp_index").val(1);
	}else{
		var index = 0;
		for(i in sp_object){
			index = i;
			sp_html += sellPriceHtmlForValues(i, sp_object[i]["price"], sp_object[i]["currency"]);
		}
		sp_html += "</div>";
		index = parseInt(index) + 1;
		$("#sp_index").val(index);
	}
	return sp_html;
}

function sellPriceHtmlForValues(sp_row_id, price, currency, campaign){
	var sp_html =  "<div id='sp_"+sp_row_id+"'>"
	 	+"<input type='button' onclick='addSellPrice()' value='+' style='font-size:1.5em;color:#00FF00' />"
	 	+"<input type='button' onclick='removeSellPrice("+sp_row_id+")' value='-' style='font-size:1.5em;color:#FF0000' />"
	 	+"<label style='font-weight:bold;font-size:1.1em'>Price :&nbsp;</label>"
	 	+"<input type='text' maxlength='10' size='11' id='sp_price' value='"+price+"'/>&nbsp;"
	 	+"<label style='font-weight:bold;font-size:1.1em'>Currency :&nbsp;</label>"
	 	+"<select id='sp_currency'>";
		for(var idx in currency_list){
			if(currency_list[idx] == currency){
				sp_html += "<option selected value='"+currency_list[idx]+"'>"+currency_list[idx]+"</option>";
			}else{
				sp_html += "<option value='"+currency_list[idx]+"'>"+currency_list[idx]+"</option>";
			}
		}
		
		sp_html +=  "</select>&nbsp;"				
			 		+"</div>"
	return sp_html;			 	
}

function addSellPrice(){
		var index = $("#sp_index").val();
		var sp_html = sellPriceHtmlForValues(index, 0, null, null);
		$("#main_sp_div").append(sp_html);
		index = parseInt(index) + 1;
		$("#sp_index").val(index);	
}

function removeSellPrice(index){
	$("#sp_"+index).remove();
}

function makeSellPriceJSONFromHtmlToField(){

	var sp_list = [];
	var index = parseInt($("#sp_index").val());
	for(i=0; i < index;i++){
		if( $("#sp_"+i).length == 0 ){
			continue;
		}
		var sp_row_div = $("#sp_"+i); 
		
		var sp_data = {};
		sp_data["price"] = parseInt(sp_row_div.find("#sp_price").val());
		sp_data["currency"] = sp_row_div.find("#sp_currency").val();

		sp_list.push(sp_data);
	}
	if(sp_list.length == 0){
		$("#id_sell_price").val("");
	}else{
		$("#id_sell_price").val(JSON.stringify(sp_list));
	}
}