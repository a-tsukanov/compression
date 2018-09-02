window.onload = () => {
    $('#submit').click(() => {
        if ($('#p').val().length === 0 ||
            $('#q').val().length === 0 ||
            $('#s').val().length === 0 ||
            $('#t').val().length === 0)
        {
            alert('Пожалуйста, заполните все параметры: S, P, Q и t');
            $("form").submit((e) => {
                e.preventDefault();
            });
        }
    });
};
