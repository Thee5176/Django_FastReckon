// must specify 'elementQuery' before import this code
if (typeof elementQuery !== "undefined") {
    var el = document.querySelectorAll(elementQuery);
    var sum = 0;

    console.log("Retrived amount element", el)

    for (var element of el) {
        value = element.innerText.trim()
        sum += parseFloat(value) || 0;
        console.log(sum)
    }

    document.write(sum);
} else {
    console.error("elementQuery is not defined.");
}