$(document).ready(function(){
	$("body").fadeIn("fast");
/*
	var t = document.getElementById("error_or_alert");
	if (t.innerHTML === "") {
		console.log("empty");
	} else {
		$("#error_or_alert").parent().fadeIn("slow");
	}

	$('input[type=file]').bootstrapFileInput();*/
	bool_to_img();
	
	/*if (window.location.href === "http://localhost:8181/user/show_me_my_lot/") {
		my_lots_checkbox()
		del_my_lot()
	}*/

	var li_el = $(".place_for_prev li img");
	
	var i;

	for (i = 0; i < li_el.length; i++) {
		li_el[i].onclick = change_full_img;
	}

	function change_full_img() {
		$("#full_img_viv").hide();
		$("#full_img_viv")[0].src = this.src;
		$("#full_img_viv").fadeIn("fast");
	}

});

function this_location_select(){
	var links = $('a');
	var location = window.location.href;
	var i = 0;
	for( i = 0; i < links.length; i++) {
		if (links[i].href === location) {
			$(links[i]).addClass("menu_a_active");
			$(links[i]).parent().addClass("menu_li_active");
		}}}

this_location_select();

function bool_to_img() {
	var p = document.getElementsByClassName('my_lots_boolean'); //$('.my_lots_boolean');
	for (var i = 0; i < p.length; i++) {
		if (p[i].innerHTML === "False") {
			var this_img = $(p[i]).parent().children('img');
			this_img[0].src = "http://localhost:8181/static/img/no.png";
		} else if (p[i].innerHTML === "True") {
			var this_img = $(p[i]).parent().children('img');
			this_img[0].src = "http://localhost:8181/static/img/yes.png";
		}
	}
}

/*function my_lots_checkbox() {
	var chb = document.getElementById('header_chb');
	var all_chb = document.getElementsByTagName('input')
	chb.onclick = my_lots_checkbox_check;
		function my_lots_checkbox_check() {
			if (chb.checked) {
				for (var i = 0; i < all_chb.length; i++) {
					all_chb[i].checked = true;
				}
			} else for (var i = 0; i < all_chb.length; i++) {
					all_chb[i].checked = false;
				}
		}
}*/

function del_my_lot() {
	var del_button = $("#del_my_lot");
	var absolute_url_args;
	var absolute_url;
	del_button.click(del_deter_func);
	function del_deter_func() {
		var massivee = [];
		var chbx = $("input[type = 'checkbox']")
		for (var i = 1; i < chbx.length; i++) {
			if (chbx[i].checked) {
				this_el = $(chbx[i]).parent("td").parent("tr").children("td");
				absolute_url_args = $(this_el[1]).text();
				massivee.push(absolute_url_args);
			}
		}
		var url = "http://localhost:8181/user/dellot/";
		massivee = massivee.join("_");
		absolute_url = url + massivee + "/";
		if (massivee === "") {
			alert("Выберите что нужно удалить");
		} else if (confirm("Вы уверены что хотите удалить ???????")) {
			window.location.href = absolute_url;			
		}

		
		
	}
}

function edit_lot() {
	var lot = $('tr');
	for(var i = 1; i < lot.length; i++) {
		this_tr = lot[i];
		for (var e = 1; e < $(this_tr).children().length; e++) {
			$(this_tr).children()[e].onclick = ret_to_edit;
		}
	}
		function ret_to_edit() {
				var this_el = $(this).parent().children("td")[1];
				this_el = $(this_el).text();
				var absolute_url = "http://localhost:8181/user/editlot/" + this_el + "/";
				window.location.href = absolute_url;
		}
}

function soort() {
	var seleect = $("#sort_by");
	$(seleect).change(run_soted);
	var trs_arr = [];
	function run_soted() {
		if (seleect.val() === "3") {
			var trs = $("tr");
			for (var i = 1; i < trs.length; i++) {
				var intermediate = $(trs[i]).children("td");
				for (var e = 2; e < 6;) {
					console.log(intermediate[e]);
					
				}
			}
		}
	}
}

function show_popup_seller_email_func() {
	var btn = $("#show_popup_seller_email");
	$(btn).click(( function() {
		$(".popup-bg").fadeIn("slow");
	} ))
	var pop_bg = $(".popup-bg").click((function() {
		pop_bg.fadeOut("fast")
	} ))
}


show_popup_seller_email_func();
soort();
del_my_lot();
edit_lot();
//my_lots_checkbox();