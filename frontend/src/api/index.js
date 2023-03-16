class Api {
  constructor (url, headers) {
    this._url = url
    this._headers = headers
  }

  checkResponse (res) {
    return new Promise((resolve, reject) => {
      if (res.status === 204) {
        return resolve(res)
      }
      const func = res.status < 400 ? resolve : reject
      res.json().then(data => func(data))
    })
  }

  checkFileDownloadResponse (res) {
    return new Promise((resolve, reject) => {
      if (res.status < 400) {
        return res.blob().then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = "shopping-list";
          document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
          a.click();    
          a.remove();  //afterwards we remove the element again 
        })
      }
      reject()
    })
  }

  signin ({ email, password }) {
    return fetch(
      '/api/auth/token/login/',
      {
        method: 'POST',
        headers: this._headers,
        body: JSON.stringify({
          email, password
        })
      }
    ).then(this.checkResponse)
  }

  signout () {
    const token = localStorage.getItem('token')
    return fetch(
      '/api/auth/token/logout/',
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  signup ({ email, password, username, first_name, last_name }) {
    return fetch(
      `/api/users/`,
      {
        method: 'POST',
        headers: this._headers,
        body: JSON.stringify({
          email, password, username, first_name, last_name
        })
      }
    ).then(this.checkResponse)
  }

  getUserData () {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/users/me/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  changePassword ({ current_password, new_password }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/users/set_password/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify({ current_password, new_password })
      }
    ).then(this.checkResponse)
  }


  // recipes

  getRecipes ({
    page = 1,
    limit = 6,
    is_favorited = 0,
    is_in_shopping_cart = 0,
    author,
    Tag
  } = {}) {
      const token = localStorage.getItem('token')
      const authorization = token ? { 'authorization': `Token ${token}` } : {}
      const TagString = Tag ? Tag.filter(tag => tag.value).map(tag => `&Tag=${tag.slug}`).join('') : ''
      return fetch(
        `/api/recipes/?page=${page}&limit=${limit}${author ? `&author=${author}` : ''}${is_favorited ? `&is_favorited=${is_favorited}` : ''}${is_in_shopping_cart ? `&is_in_shopping_cart=${is_in_shopping_cart}` : ''}${TagString}`,
        {
          method: 'GET',
          headers: {
            ...this._headers,
            ...authorization
          }
        }
      ).then(this.checkResponse)
  }

  getRecipe ({
    recipe_id
  }) {
    const token = localStorage.getItem('token')
    const authorization = token ? { 'authorization': `Token ${token}` } : {}
    return fetch(
      `/api/recipes/${recipe_id}/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          ...authorization
        }
      }
    ).then(this.checkResponse)
  }

  createRecipe ({
    name = '',
    image,
    Tag = [],
    cooking_time = 0,
    text = '',
    ingredient = []
  }) {
    const token = localStorage.getItem('token')
    return fetch(
      '/api/recipes/',
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify({
          name,
          image,
          Tag,
          cooking_time,
          text,
          ingredient
        })
      }
    ).then(this.checkResponse)
  }

  updateRecipe ({
    name,
    recipe_id,
    image,
    Tag,
    cooking_time,
    text,
    ingredient
  }, wasImageUpdated) { // image was changed
    const token = localStorage.getItem('token')
    return fetch(
      `/api/recipes/${recipe_id}/`,
      {
        method: 'PATCH',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify({
          name,
          id: recipe_id,
          image: wasImageUpdated ? image : undefined,
          Tag,
          cooking_time: Number(cooking_time),
          text,
          ingredient
        })
      }
    ).then(this.checkResponse)
  }

  addToFavorites ({ id }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/recipes/${id}/favorite/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  removeFromFavorites ({ id }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/recipes/${id}/favorite/`,
      {
        method: 'DELETE',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  getUser ({ id }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/users/${id}/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  getUsers ({
    page = 1,
    limit = 6
  }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/users/?page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // subscriptions

  getSubscriptions ({
    page, 
    limit = 6,
    recipes_limit = 3
  }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/users/subscriptions/?page=${page}&limit=${limit}&recipes_limit=${recipes_limit}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  deleteSubscriptions ({
    author_id
  }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/users/${author_id}/subscribe/`,
      {
        method: 'DELETE',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  subscribe ({
    author_id
  }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/users/${author_id}/subscribe/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // ingredient
  getingredient ({ name }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/ingredient/?name=${name}`,
      {
        method: 'GET',
        headers: {
          ...this._headers
        }
      }
    ).then(this.checkResponse)
  }

  // Tag
  getTag () {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/Tag/`,
      {
        method: 'GET',
        headers: {
          ...this._headers
        }
      }
    ).then(this.checkResponse)
  }


  addToOrders ({ id }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/recipes/${id}/shopping_cart/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  removeFromOrders ({ id }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/recipes/${id}/shopping_cart/`,
      {
        method: 'DELETE',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  deleteRecipe ({ recipe_id }) {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/recipes/${recipe_id}/`,
      {
        method: 'DELETE',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  downloadFile () {
    const token = localStorage.getItem('token')
    return fetch(
      `/api/recipes/download_shopping_cart/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkFileDownloadResponse)
  }
}

export default new Api(process.env.API_URL || 'http://localhost', { 'content-type': 'application/json' })
