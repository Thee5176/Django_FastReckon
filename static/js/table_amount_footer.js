// must specify 'classQuery' before import this code
if (typeof classQuery !== "undefined") {
    var el = document.getElementsByClassName(classQuery);
    var sum = 0;

    console.log("Retrived amount element", el)

    for (var element of el) {
        value = element.innerText.trim()
        sum += parseFloat(value) || 0;
        console.log(sum)
    }

    document.write(sum);
} else {
    console.error("classQuery is not defined.");
}