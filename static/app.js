const $list = $("#list");
const $form = $("#form-cupcake");
const base_url = '/api/cupcakes';

async function get_list() {
    const response = await axios.get(base_url);

    return response;
}

async function create() {
    const response = await axios.post(base_url,
        {
            "flavor": $("#flavor").val(),
            "size": $("#size").val(),
            "image": $("#image").val(),
            "rating": $("#rating").val()
        }
    );
    return response;
}

$form.on("submit", async function (e) {
    e.preventDefault();

    res = await create();

    if (res.status == 201){
        $list.append(get_list_html(res.data.cupcake));
        $form.trigger("reset");
    } else {
        //error
        alert("Error when updating!")
    }

});


async function on_load() {
    res = await get_list();

    items = res.data.cupcakes;

    for (item of items) {
        listTemplate = get_list_html(item);
        $list.append(listTemplate);
    }
}

function get_list_html(item) {
    return `
    <div data-id='${item.id}'>
        <img src='${item.image}'  class="img-fluid img-thumbnail rounded" />
        <div class="fs-5">
            <p><label class='fw-bold'>Flavor:</label> ${item.flavor}</p>
            <p><label class='fw-bold'>Size:</label>  ${item.flavor}</p>
            <p><label class='fw-bold'>Rating:</label>  ${item.rating}</p>
        </div>
    </div>
        `;
}


on_load();