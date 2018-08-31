$('#file_chooser').on("change", () => {
    const file = document.getElementById('file_chooser').files[0];
    if (file) {
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = (e) => {
            const text = e.target.result;
            document.getElementById("text_to_compress").innerText = text;
        };
    }
});