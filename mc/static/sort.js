/* 
* 常用三种类型转换(int float date string)： 
* sValue 要转换的值 
* sDataType 要转换的值的类型 
*/  
function convert(sValue, sDataType) {  
    switch (sDataType) {  
      case "int"://整型  
        return parseInt(sValue);  
      case "float"://浮点型  
        return parseFloat(sValue);  
      case "date"://日期型  
        return new Date(Date.parse(sValue));  
      default://任何其他类型返回字符串  
        return sValue.toString();  
    }  
}  
/* 
* 创建比较函数方法，这里采了闭包的方式，生成的比较函数根据所比较的列编号 
* 与列数组类型不同而不同。 
* iCol 要进行比较的列编号 
* sDataType 列数据类型 
*/  
function generateCompareTRs(iCol, childNumber, sDataType) {
    /*真真的比较函数，供数组的sort方法调用，oTR1 oTR2两个参数由sort方法传进来 
    oTR1为比较的第一行，oTR2为比较的第二行*/  
    return function compareTRs(oTR1, oTR2) {  
    	//alert(oTR1.cells[iCol].childNodes[1].childNodes[1].firstChild.nodeValue);
    	if (childNumber == 1) {   		
    		if (oTR1.cells[iCol].firstChild.firstChild != null){
    			var vValue1 = convert(oTR1.cells[iCol].firstChild.firstChild.nodeValue, sDataType);
    		}
    		else {
    			var vValue1 = oTR1.cells[iCol].firstChild.nodeValue;
    		}
    		
    		if (oTR2.cells[iCol].firstChild.firstChild != null){
    			var vValue2 = convert(oTR2.cells[iCol].firstChild.firstChild.nodeValue, sDataType);
    		}
    		else {
    			var vValue2 = oTR2.cells[iCol].firstChild.nodeValue;
    		}    		
    	}
    	else if (childNumber == 2) {
            var vValue1 = convert(oTR1.cells[iCol].firstChild.firstChild.firstChild.nodeValue, sDataType); 
            var vValue2 = convert(oTR2.cells[iCol].firstChild.firstChild.firstChild.nodeValue, sDataType);
    	}
    	else {
            var vValue1 = convert(oTR1.cells[iCol].firstChild.nodeValue, sDataType);
            var vValue2 = convert(oTR2.cells[iCol].firstChild.nodeValue, sDataType);
    	}
        //按升序比较，如果是日期类型时会自动调用其valueOf方法返date 的毫秒再进行比较  
    	if (vValue1 == null && vValue2 == null) {
    		return 0;
    	}
    	if (vValue1 == null) {
    		return -1;
    	}
    	if (vValue2 == null) {
    		return 1;
    	}
        if (vValue1 < vValue2) {  
            return -1;  
        }
        else {  
        	if (vValue1 > vValue2) {  
                return 1;  
            } 
        	else {  
                return 0;  
            }  
        }  
    };  
}  
/* 
* 表格比较，由HTML点击事件调用 
* sTableID 要比较的表格id 
* iCol 要较的表格的列的编号 
* sDataType 列的数据类型 
*/  
function sortTable(sTableID, iCol, childNumber, sDataType) {
    if($('#list_sort').attr('class')=="nosort"){
        $('#list_sort').removeClass();
        $('#list_sort').addClass('sort_asc');
    }else if($('#list_sort').attr('class')=="sort_asc"){
        $('#list_sort').removeClass();
        $('#list_sort').addClass('sort_desc');
    }else if($('#list_sort').attr('class')=="sort_desc"){
        $('#list_sort').removeClass();
        $('#list_sort').addClass('sort_asc');
    }
    //获取表格对象  
    var oTable = document.getElementById(sTableID);
    
    //获取表格体  
    var oTBody = oTable.tBodies[0];  
    
    //获取表格体中所有行  
    var colDataRows = oTBody.rows;
    
    //存储所有表格行，借且于数组来进行排序处理  
    var aTRs = new Array;  
             
    //把所有的行存储到数组里  
    for (var i = 0; i < colDataRows.length; i++) {  
        aTRs[i] = colDataRows[i];  
    }  

    /*sortCol为表格的扩展属性，标示最后是根据哪列来进行排序的。 
    如果要传进来的列与上次排序的列是同一列时，直接对数组进行 
    reverse反序操作，这样排序的速度会更快*/  
    if (oTable.sortCol == iCol) {  
        aTRs.reverse();
    } else {  
    //如果是第一次排序，则调用排序算法进行排序  
        aTRs.sort(generateCompareTRs(iCol, childNumber, sDataType));
    }  
                          
    //创建文档碎片，这样不用一个一个把行添加到表格对象中，而是一次就可以了  
    var oFragment = document.createDocumentFragment();  
    for (var i = 0; i < aTRs.length; i++) {  
        oFragment.appendChild(aTRs[i]);  
    }  
   
    //把所排序的行重样追加到表格对象中，注：这里没有单独先删除表格排序前的行  
    //因为如果追加的行是一样的话，appendChild操作会先自动删除后再添加。  
    oTBody.appendChild(oFragment);  
    oTable.sortCol = iCol;  
}

function addTableSortJs(tableIds) {
    for (var index in tableIds) {
    	var cl = tableIds[index];
    	var st = "table#" + cl + ">thead>tr>th";

        $(st).click(function(event){
            if ($(this).hasClass("t_asc")){
            	$(this).removeClass("t_asc").addClass("t_desc");
            } else if ($(this).hasClass("t_desc")){
            	$(this).removeClass("t_desc").addClass("t_asc");
            } else {
            	$(this).addClass("t_asc").siblings().removeClass("t_asc").removeClass("t_desc");
            }
        });	
    }
}

//$(document).ready(function() {
//	var tableIds = eval(table_id);
//	addTableSortJs(tableIds);
//
//});
