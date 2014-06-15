function insertMultiValueHtml(enabled_name_edit){
	$("#ca_main_div").remove();	
	var ca_html = "<div id='ca_main_div'>";
	var index = 0;

	if($("#id_type_meta_data").val() === undefined || $("#id_type_meta_data").val() == null || $("#id_type_meta_data").val() == ""){
		ca_html += subAttributeHtmlForValue(index, null, enabled_name_edit);
	}else{
		// parse value
		var sub_attribute_names = JSON.parse($("#id_type_meta_data").val());
		
		for(idx in sub_attribute_names){
			ca_html += subAttributeHtmlForValue(idx, sub_attribute_names[idx], enabled_name_edit);
			index = idx;
		}
	}

	ca_html += "<input id='ca_main_div_add_button' type='button' value='Add Sub Attribute' onclick='addSubAttribute()' />";
	ca_html += "</div>";
	index = parseInt(index)+1;
	$("#ca_index").val(index);
	$("#multi_value_html").html(ca_html);
}

function removeSubAttribute(idx){
	$("#ca_"+idx).remove();
}

function addSubAttribute(){
	var index = $("#ca_index").val();
	ca_html =   subAttributeHtmlForValue(index, null,true);
	ca_html += "<input id='ca_main_div_add_button' type='button' value='Add Sub Attribute' onclick='addSubAttribute()' />";
	index = parseInt(index) + 1;
	$("#ca_index").val(index);
	$("#ca_main_div_add_button").remove();
	$("#ca_main_div").append(ca_html);
}

function subAttributeHtmlForValue(idx, name, enabled_name_edit){
	
	sa_html =  "<div id='ca_"+idx+"'>"					
				+"<input type='button' value='-' style='font-size:1.1em;color:#FF0000;' onclick='removeSubAttribute("+idx+")' />"
				+"<input type='text' id='ca_value' "+(enabled_name_edit == true ? "": "disabled='true'")+"' onkeypress='return alphanumwithoutspace(event, this)' value='"+(name == null ? "" : name) +"' max_length=50 size='50' />"
			    +"</div>";
	return sa_html;
}

function makeMultiValueJSONFromHtml(){

	var ca_list = [];
	var index = parseInt($("#ca_index").val());
	for(i=0; i < index;i++){
		if( $("#ca_"+i).find("#ca_value").val() === undefined || $("#ca_"+i).find("#ca_value").val() == "" || $("#ca_"+i).find("#ca_value").val() == null ){
			continue;
		}
		var ca_row_div = $("#ca_"+i);
		ca_list.push(ca_row_div.find("#ca_value").val());
	}
	
	if(ca_list.length > 0){
		$("#id_type_meta_data").val(JSON.stringify(ca_list));
	}else{
		$("#id_type_meta_data").val("");
	}
	return true;
}

function updateCustomAttributeWidget(custom_attribute){
	switch(custom_attribute["widget"]){
	
	case "number":
		setNumberWidget(custom_attribute);
		break;
	
	case "text":
		setTextWidget(custom_attribute);
		break;
		
	case "datetime":
		setDateTimeWidget(custom_attribute);
		break;
		
	case "boolean":
		setBooleanWidget(custom_attribute);
		break;
		
	case "currency":
		setCurrencyWidget(custom_attribute);
		break;
		
	case "multivalue":
		setMultiValueWidget(custom_attribute);
		break;
	}
}

function setNumberWidget(custom_attribute){
	
	widget_html = "<input type='text' onkeypress='return floatnum()' id='"+custom_attribute["id"]+"'"
				+" name='"+custom_attribute["name"]+"'"
				+" value='"+(isNullOrEmptyOrUndefined(custom_attribute["widget_value"]) == true ? "" : custom_attribute["widget_value"] )+"'"
				+" />";
	
	$("#"+custom_attribute["id"]).replaceWith(widget_html);	
}

function setTextWidget(custom_attribute){
	
	widget_html = "<input type='text' id='"+custom_attribute["id"]+"'"
				+" name='"+custom_attribute["name"]+"'"
				+" value='"+(isNullOrEmptyOrUndefined(custom_attribute["widget_value"]) == true ? "" : custom_attribute["widget_value"] )+"'"
				+" />";
	
	$("#"+custom_attribute["id"]).replaceWith(widget_html);	
}

function setBooleanWidget(custom_attribute){
	
	widget_html = "<select id='"+custom_attribute["id"]+"' name='"+custom_attribute["name"]+"'>" 
				  +"<option value='0' "+(custom_attribute["widget_value"] == '0' ? "selected" : "")+">False</option>"
				  +"<option value='1' "+(custom_attribute["widget_value"] == '1' ? "selected" : "")+">True</option>"
				  +"</select>";	
	$("#"+custom_attribute["id"]).replaceWith(widget_html);	
}

function setCurrencyWidget(custom_attribute){
	
	widget_html = "<select id='"+custom_attribute["id"]+"' name='"+custom_attribute["name"]+"'>";
	
		for(i in currency_list){
			widget_html += "<option value='"+currency_list[i]+"' "+(custom_attribute["widget_value"] == currency_list[i] ? "selected" : "")+">"+currency_list[i]+"</option>"
		}
		+"</select>";	
	$("#"+custom_attribute["id"]).replaceWith(widget_html);	
}

function setDateTimeWidget(custom_attribute){
	var now = new Date();
	date_str =  now.getFullYear()+'-'
				+(now.getMonth()+1)+'-'
				+(now.getDate() < 10 ? "0"+now.getDate(): now.getDate())
				+" "
				+(now.getHours() < 10 ? "0"+now.getHours(): now.getHours())
				+":"
				+(now.getMinutes() < 10 ? "0"+now.getMinutes(): now.getMinutes())
				+":"
				+(now.getSeconds() < 10 ? "0"+now.getSeconds(): now.getSeconds());
	widget_html = "<input type='text' id='"+custom_attribute["id"]+"'"
					+" name='"+custom_attribute["name"]+"' readonly='true'"
					+" value='"+(isNullOrEmptyOrUndefined(custom_attribute["widget_value"]) == true ? date_str : custom_attribute["widget_value"] )+"'"
					+" />";


	$("#"+custom_attribute["id"]).replaceWith(widget_html);
	$(function() {
		$('#'+custom_attribute["id"]).datetimepicker(
				{	showSecond: false,
					timeFormat: 'hh:mm:ss',
					stepHour: 1,
					stepMinute: 1});
		});
	
}

function setMultiValueWidget(custom_attribute){
	
	var widget_html = 	"<input type='text' id='"+custom_attribute["id"]+"'"
						+" name='"+custom_attribute["name"]+"' "
						+" value='"+(isNullOrEmptyOrUndefined(custom_attribute["widget_value"]) == true ? "" : custom_attribute["widget_value"] )+"'"
						+" onclick='showMultiValuePopupForIndex("+custom_attribute["index"]+")'"
						+" readonly='true' />"
						
    $("#"+custom_attribute["id"]).replaceWith(widget_html);
}

function showMultiValuePopupForIndex(idx){
	var mv_meta = custom_attributes[idx];
	var mv_html = "<div id='"+mv_meta["id"]+"_main_div' style='overflow:auto;max-height:20em;max-width:80em;'>";
	var mv_json = $("#"+mv_meta["id"]).val();
	var mv_obj = null;
	var index = 0;
	
	if(isNullOrEmptyOrUndefined(mv_json) == true){
		// show empty popup
		if(mv_meta['label'] == 'listitem'){
			mv_html += getMultiValueFieldRowForLuckyBoxValues(index, mv_meta["id"], JSON.parse(mv_meta["widget_meta"]), null, idx);
		}else{
			mv_html += getMultiValueFieldRowForValues(index, mv_meta["id"], JSON.parse(mv_meta["widget_meta"]), null, idx);
		}
	}else{
		mv_obj = JSON.parse(mv_json);
		for(i in mv_obj){
			if(mv_meta['label'] == 'listitem'){
				mv_html += getMultiValueFieldRowForLuckyBoxValues(index, mv_meta["id"], JSON.parse(mv_meta["widget_meta"]), mv_obj[i], idx);
			}else{
				mv_html += getMultiValueFieldRowForValues(index, mv_meta["id"], JSON.parse(mv_meta["widget_meta"]), mv_obj[i], idx);
			}
			
			index = parseInt(index) + 1;
		}
	}
	
	mv_html += "</div>";
	index = parseInt(index) + 1;
	$("#mv_index").val(index);
	jEmpty(mv_html, mv_meta["label"], function(result){ if(result){ makeJSONFromMultiValueToField(idx); }});
}

function getMultiValueFieldRowForValues(row_index, row_id, row_meta, row_value, meta_index){
	
	var mv_row = "<div id='"+row_id+"_"+row_index+"'>"
				+"<input type='button' onclick='addMultiValueRowForIndex("+meta_index+")' value='+' style='font-size:1.5em;color#00FF00' />"
			 	+"<input type='button' onclick='removeMultiValueRow(\""+row_id+"_"+row_index+"\")' value='-' style='font-size:1.5em;color:#FF0000' />";
	if( isNullOrEmptyOrUndefined(row_value)){	
		for(i in row_meta){
			mv_row += "<label style='font-weight:bold;font-size:1.1em'>"+row_meta[i]+" :&nbsp;</label>"
		 			  +"<input type='text' style='width:7em' id='mv_value"+row_meta[i]+"' value=''/>&nbsp;"
		}
	}else{
		for(i in row_meta){
			mv_row += "<label style='font-weight:bold;font-size:1.1em'>"+row_meta[i]+" :&nbsp;</label>"
		 			  +"<input type='text' style='width:7em' id='mv_value"+row_meta[i]+"' value='"+row_value[row_meta[i]]+"'/>&nbsp;"
		}
	}
	mv_row += "</div>";
	return mv_row;
}

/* again hardcoding it...should make it generic in future */

function getMultiValueFieldRowForLuckyBoxValues(row_index, row_id, row_meta, row_value, meta_index){
	
	var mv_row = "<div id='"+row_id+"_"+row_index+"'>"
				+"<input type='button' onclick='addMultiValueRowForIndex("+meta_index+")' value='+' style='font-size:1.5em;color#00FF00' />"
			 	+"<input type='button' onclick='removeMultiValueRow(\""+row_id+"_"+row_index+"\")' value='-' style='font-size:1.5em;color:#FF0000' />";
	if( isNullOrEmptyOrUndefined(row_value)){	
		for(i in row_meta){
			if(row_meta[i] == 'storeid'){
				mv_row += "<label style='font-weight:bold;font-size:1.1em'>"+row_meta[i]+" :&nbsp;</label>"
		 			  +makeDropDownForLuckyBox("mv_value"+row_meta[i], luckybox_data, null)+"&nbsp;"
			}else{
				mv_row += "<label style='font-weight:bold;font-size:1.1em'>"+row_meta[i]+" :&nbsp;</label>"
	 			  +"<input type='text' style='width:7em' id='mv_value"+row_meta[i]+"' value=''/>&nbsp;"
			}
		}
	}else{
		for(i in row_meta){
			if(row_meta[i] == 'storeid'){
				mv_row += "<label style='font-weight:bold;font-size:1.1em'>"+row_meta[i]+" :&nbsp;</label>"
		 			  +makeDropDownForLuckyBox("mv_value"+row_meta[i], luckybox_data, row_value[row_meta[i]])+"&nbsp;"
			}else{
				mv_row += "<label style='font-weight:bold;font-size:1.1em'>"+row_meta[i]+" :&nbsp;</label>"
	 			  +"<input type='text' style='width:7em' id='mv_value"+row_meta[i]+"' value='"+row_value[row_meta[i]]+"'/>&nbsp;"
			}
		}
	}
	mv_row += "</div>";
	return mv_row;
}

function addMultiValueRowForIndex(idx){
	var mv_meta = custom_attributes[idx];
	var index = $("#mv_index").val();
	var mv_html = null;
	if(mv_meta['label'] == 'listitem'){
		mv_html = getMultiValueFieldRowForLuckyBoxValues(index, mv_meta["id"], JSON.parse(mv_meta["widget_meta"]), null, idx);
	}else{
		mv_html = getMultiValueFieldRowForValues(index, mv_meta["id"], JSON.parse(mv_meta["widget_meta"]), null, idx);
	}
	
	index = parseInt(index) + 1;
	$("#mv_index").val(index);
	$("#"+mv_meta["id"]+"_main_div").append(mv_html);
}

function removeMultiValueRow(mv_row_id){
	$("#"+mv_row_id).remove();
}

function makeJSONFromMultiValueToField(idx){
	var mv_meta = custom_attributes[idx];
	var mv_data = JSON.parse(mv_meta["widget_meta"]);
	var cv_list = [];
	var index = parseInt($("#mv_index").val());
	for(i=0; i < index;i++){
		if( $("#"+mv_meta["id"]+"_"+i).length == 0 ){
			continue;
		}
		var cv_row_div = $("#"+mv_meta["id"]+"_"+i); 
		
		var cv_data = {};
		for(j in mv_data){
			var row_val = cv_row_div.find("#mv_value"+mv_data[j]).val();
			cv_data[mv_data[j]] = row_val == null ? "" : row_val;
		}
		cv_list.push(cv_data);
	}
	if(cv_list.length == 0){
		$("#"+mv_meta["id"]).val("");
	}else{
		$("#"+mv_meta["id"]).val(JSON.stringify(cv_list));
	}
}

/* hard-coding for the quick fix.. arrrrggghhh, will make it generic later */
function makeDropDownForBreededFish(field_name, breeded_data, selected_key){
	var breeded_html = "<select id='id_"+field_name+"' name='"+field_name+"'><option value='' >---</option>";
	var keys = [];
	for (var key in breeded_data) {
	    keys.push(key);
	}
	keys.sort();
	for(var i in keys){
		var key = keys[i];
		breeded_html += "<option value='"+breeded_data[key];
		if (selected_key == breeded_data[key] ){
			breeded_html += "' selected ";
		}
		breeded_html += "'>"+key+"</option>";
	}
	
	breeded_html += "</select>"
	
	$("#id_"+field_name).replaceWith(breeded_html);
}

function makeDropDownForLuckyBox(field_name, luckybox_data, selected_key, make_id){
	var luckybox_html = null;
	if(typeof(make_id)=== 'undefined'){
		luckybox_html = "<select id='"+field_name+"' name='"+field_name+"'>";
	}else{
		luckybox_html = "<select id='id_"+field_name+"' name='"+field_name+"'><option value=''>---</option>";
	}
	
	var keys = [];
	for (var key in luckybox_data) {
	    keys.push(key);
	}
	keys.sort();
	for(var i in keys){
		var key = keys[i];
		luckybox_html += "<option value='"+luckybox_data[key];
		if (selected_key == luckybox_data[key] ){
			luckybox_html += "' selected ";
		}
		luckybox_html += "'>"+key+"</option>";
	}
	
	luckybox_html += "</select>"
	return luckybox_html;
}