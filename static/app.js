const $list = $("#list");
const $formTitle = $("#form-title");
const $form = $("#form-cupcake");
const $btnAdd = $("#btn-add");
const base_url = '/api/cupcakes';

let isFormEdit = false;
let currentId = 0;
let $currentElement = null;

async function get_list() {
    const response = await axios.get(base_url);

    return response;
}

async function update() {
    if (isFormEdit === false) {
        const response = await axios.post(base_url,
            {
                "flavor": $("#flavor").val(),
                "size": $("#size").val(),
                "image": $("#image").val(),
                "rating": $("#rating").val()
            }
        );
        return response;
    } else {
        const response = await axios.patch(base_url + "/" + currentId,
            {
                "flavor": $("#flavor").val(),
                "size": $("#size").val(),
                "image": $("#image").val(),
                "rating": $("#rating").val()
            }
        );
        return response;
    }
}

async function delCupcake(id) {
    const response = await axios.delete(base_url + "/" + id);

    return response;
}

$form.on("submit", async function (e) {
    e.preventDefault();

    res = await update();

    if (res.status === 201) {
        $list.append(get_list_html(res.data.cupcake));
        $form.trigger("reset");
    } else if (res.status === 200) {
        $btnAdd.trigger("click");

        $currentElement.replaceWith(get_list_html(res.data.cupcake));
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
    <div 
    data-id='${item.id}' data-flavor='${item.flavor}' data-rating='${item.rating}'
    data-size='${item.size}' data-image='${item.image}' 
    class='list-item'>
        <p class='position-absolute float-right h5'>
            <a href="javascript:void(0)" title='Edit' class="list-edit text-primary"><i class="far fa-edit m-2"></i></a>
            <a href="javascript:void(0)" title='Delete' class="list-delete text-danger"><i class="far fa-trash-alt m2"></i></a></p>
        <img src='${item.image}'  class="img-fluid img-thumbnail rounded" />
        <div class="fs-5">
            <p><label class='fw-bold'>Flavor:</label> ${item.flavor}</p>
            <p><label class='fw-bold'>Size:</label>  ${item.size}</p>
            <p><label class='fw-bold'>Rating:</label>  ${item.rating}</p>
        </div>
    </div>
        `;
}

on_load();


$(document).on("click", ".list-edit", async (e) => {
    e.preventDefault();
    $button = $(e.target);
    $item = $button.parents(".list-item");

    $formTitle.html("Edit Cupcake");
    $form.trigger("reset");

    isFormEdit = true;
    currentId = $item.data("id");
    $currentElement = $item;

    $("#flavor").val($item.data("flavor"));
    $("#size").val($item.data("size"));
    $("#rating").val($item.data("rating"));
    $("#image").val($item.data("image"));

    $(document).scrollTop($form.offset().top);
    $btnAdd.removeClass("d-none");
});

$(document).on("click", ".list-delete", async (e) => {
    e.preventDefault();

    $button = $(e.target);
    $item = $button.parents(".list-item");

    id = $item.data("id");

    res = await delCupcake(id);

    if (res.status === 200) {
        $item.remove();
    } else {
        //error
        alert("Error when updating!")
    }

});

$btnAdd.on("click" , (e) => {
    isFormEdit = false;
    $formTitle.text("Add a Cupcake");
    $form.trigger("reset");
    $btnAdd.addClass("d-none");
});
