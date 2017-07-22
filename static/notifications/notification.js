function gen_notification_list(data) {
    var menu = document.getElementById(notify_menu_id);
    if (menu) {
        menu.innerHTML = "";
        for (var i = 0; i < data.unread_list.length; i++) {
            var item = data.unread_list[i];
            console.log(item);
            var message = "";
            var actor = "";
            var verb = "";
            var order_id = "";
            var datetime = "";
            var status = null;
            // Get data
            var unread = item.unread;

            if (typeof item.actor != 'undefined') {
                actor = item.actor;
            }
            if (typeof item.verb != 'undefined') {
                verb = item.verb;
            }
            if (typeof item.timestamp != 'undefined') {
                datetime = item.timestamp;
            }
            if (typeof item.data != 'undefined') {
                obj = JSON.parse(item.data);
                if (typeof obj.status != 'undefined') {
                    status = obj.status;
                }
                if (typeof obj.order_id != 'undefined') {
                    order_id = obj.order_id;
                }
            }

            // Produce message
            if (verb == 'is canceled') {
                message = '<p>' + 'Đơn hàng #' + '<strong>' + order_id + '</strong>' + ' ' + '<strong>' + verb + '</strong>' + '</p>';
            } else if (verb == 'is changed') {
                message = '<p>' + 'Trạng thái của đơn hàng #' + '<strong>' + order_id + '</strong>' + ' ' + verb + ' sang ' +
                    '<strong>' + status + '</strong>' + '</p>';
            }

            // Extract time from timestamp (eg: 2016-10-22T22:10:56.102Z )
            alist = datetime.split('T');
            time = alist[1].split('.')[0].substring(0, 5);
            day = alist[0];
            datetime = day + ' ' + time;

            if (unread) {
                menu.innerHTML = menu.innerHTML + "<li class='notification active'>" + message + '<small>' + datetime + '</small>' + "</li>";
            } else {
                menu.innerHTML = menu.innerHTML + "<li class='notification'>" + message + '<small>' + datetime + '</small>' + "</li>";
            }
        }
    }
}
