import React from 'react';

const AddUser = (props) => {
  return (
    <form  onSubmit={(event) => props.addUser(event)}>
      <div className="field">
        <input
          name="username"
          className="input is-large"
          type="text"
          placeholder="Ingrese un nombre de usuario"
          required
          value={props.username}  // nuevo
          onChange={props.handleChange}
        />
      </div>
      <div className="field">
        <input
          name="email"
          className="input is-large"
          type="email"
          placeholder="Ingrese una direccion de email"
          required
          value={props.email}  // nuevo
          onChange={props.handleChange}
        />
      </div>
      <input
        type="submit"
        className="button is-danger is-rounded is-fullwidth"
        value="Submit"
      />
    </form>
  )
};

export default AddUser;
