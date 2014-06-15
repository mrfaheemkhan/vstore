function alphanum_customattribute(e)
	{
		var key = 0;

		if (window.event)
		   key = e.keyCode;

		if(key == 0)
			key = e.which

		if( isSkip(key) || (key >=48 && key <= 57) || (key >= 97  && key <= 122) || (key >= 65  && key <= 91) || (key == 95) || (key == 32)){// alphas and numbers _
			if (isValidXmlTagName($("#id_name").val()+String.fromCharCode(e.charCode)) )
		   		return true;
			else
				return false

		}else
		   return false;
	}

	function alphanum(e)
	{
		var key = 0;
	
		if (window.event)
		   key = e.keyCode;
	
		if(key == 0)
			key = e.which
	
		if( isSkip(key) || (key >=48 && key <= 57) 
				|| (key >= 97  && key <= 122) || (key >= 65  && key <= 91) 
				|| (key == 95) || (key == 32)){// alphas and numbers _			
			return true;
		}else
		   return false;
	}

	function isSkip(key)
	{
		if(key ==0 || key == 8)
			return true;
		else
			return false;
	}

	function isValidXmlTagName(tname){
		xmlStart = new RegExp("^xml", "i")
		if( xmlStart.exec(tname) != null )
			return false

		spaceStart = new RegExp("^ ", "i")
		if(spaceStart.exec(tname) != null)
			return false

		numberStart = new RegExp("^[0-9]", "i")
		if(numberStart.exec(tname) != null)
			return false

		return true

	}

	function alphanum(e, element)
	{
		var key = 0;

		if (window.event)
		   key = e.keyCode;

		if(key == 0)
			key = e.which

		if( isSkip(key) || (key >=48 && key <= 57) || (key >= 97  && key <= 122) || (key >= 65  && key <= 91) || (key == 95) || (key == 32)){// alphas and numbers _
			if (isValidXmlTagName($("#"+element.id).val()+String.fromCharCode(e.charCode)) )
		   		return true;
			else
				return false

		}else
		   return false;
	}


	function alphanumwithoutspace(e, element)
	{
		var key = 0;

		if (window.event)
		   key = e.keyCode;

		if(key == 0)
			key = e.which

		if( isSkip(key) || (key >=48 && key <= 57) || (key >= 97  && key <= 122) || (key >= 65  && key <= 91) || (key == 95) ){// alphas and numbers _
			if (isValidXmlTagName($("#"+element.id).val()+String.fromCharCode(e.charCode)) )
		   		return true;
			else
				return false

		}else
		   return false;
	}
	
	function isNullOrEmptyOrUndefined(val){
		if(val === null || val == "" || val === undefined){
			return true;
		}
		return false;		
	}