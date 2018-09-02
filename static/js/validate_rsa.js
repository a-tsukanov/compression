window.onload = () => {
    $('#submit').click(() => {
        if ($('#p').val().length === 0 ||
            $('#q').val().length === 0 ||
            $('#e').val().length === 0)
        {
            alert('Пожалуйста, заполните все параметры: P, Q и E');
            $("form").submit((e) => {
                e.preventDefault();
            });
        }
    });
};
