// Lorsque la page est chargée
window.addEventListener('DOMContentLoaded', (event) => {
  var imageElement = document.getElementById('file');
  var img = document.getElementById('apercu');
  var x_list, y_list, listeSubdivision

  const range_viewer = document.querySelector("#pas");
  const range = document.querySelector("#subdivisions");

  range_viewer.textContent = Math.pow(range.value, 2);

  range.onchange = function() {
      range_viewer.textContent = Math.pow(range.value, 2)
      localStorage.setItem("nbr_images", range.value**2)
  };


  img.onload = function() {
    var imageWidth = img.width;
    var imageHeight = img.height;
    let k = range.value

    console.log('Largeur de l\'image : ' + imageWidth);
    console.log('Hauteur de l\'image : ' + imageHeight);

    range_viewer.textContent = Math.pow(range.value, 2)
    /*console.log("x_list: "+x_list);
    console.log("y_list: "+y_list);
    console.log(nombreDeSubdivisions(x_list, y_list));*/
    // Par exemple, vous pouvez envoyer les dimensions � votre application Flask via une requ�te AJAX
  };
});

function afficherImage() {
  var input = document.getElementById('file');
  var img = document.getElementById('apercu');

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      apercu.setAttribute('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]);
  }
}

function parcoursFaisabilite(limite = 5, num = 1024, iterations = 50) {
  let n = 0;
  let i = 2;
  let possibles = [];

  while (n < limite) {
    if (num % i === 0) {
      n = n + 1;
      possibles.push(i);
    }

    i = i + 1;

    if (i >= iterations) {
      break;
    }
  }

  return [n, possibles];
}

function nombreDeSubdivisions(liste1, liste2) {
  let liste3 = [];
  for (let i of liste1) {
    for (let j of liste2) {
      if (i * j <= 100) {
        liste3.push([i, j]);
      } else {
        break;
      }
    }
  }
  liste3.sort(function(a, b) {
    //fonction de tri personnalisé pour trier des élément [11,9] > [2,41] car 11*9 > 2*41
  let produitA = a[0] * a[1];
  let produitB = b[0] * b[1];
  if (produitA < produitB) {
    return -1;
  } else if (produitA > produitB) {
    return 1;
  } else {
    return 0;
  }
  });
  return liste3;
}
