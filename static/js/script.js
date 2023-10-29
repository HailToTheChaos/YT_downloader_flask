$(document).ready(function () {
    $("#download-form").submit(function (e) {
        e.preventDefault();
        var youtube_url = $("#youtube_url").val();

        // Muestra la barra de progreso
        $(".progress").show();

        // Inicia la descarga del video
        $.ajax({
            type: "POST",
            url: "/download",
            data: { youtube_url: youtube_url },
            xhr: function () {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function (event) {
                    if (event.lengthComputable) {
                        var percentComplete = (event.loaded / event.total) * 100;
                        $("#progress-bar").css("width", percentComplete + "%");
                    }
                }, false);
                return xhr;
            },
            success: function (data) {
                // Oculta la barra de progreso y muestra el mensaje de éxito
                $(".progress").hide();
                alert(data.message);
            },
            error: function (data) {
                // Oculta la barra de progreso y muestra el mensaje de error
                $(".progress").hide();
                alert(data.responseJSON.message);
            }
        });
    });
});