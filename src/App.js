import React, {Component,} from 'react';
import './App.css';

class App extends Component {

    state = {
        customer: {
            first_name: '',
            last_name: '',
            dob: '',
            mobile: '',
            email: '',
            pdp: 'Auckland'
        },
        errors: {}
    };

    componentDidMount() {
        if (!this.state.token) {
            // fetch data
            fetch(`${process.env.REACT_APP_API_URL}/template`, {
                method: 'GET',
                header: 'Access-Control-Allow-Origin: *'
            }).then(resp => resp.json())
                .then(res => {
                    console.log(res);
                    this.setState({token: true})
                })
                .catch(error => console.log(error))
        }
    }

    inputChanged = (event) => {
        let customer = this.state.customer;
        customer[event.target.name] = event.target.value;
        this.setState({customer: customer})
    };

    sendDetails = (api_endpoint) => {
        this.checkRequired();
        console.log(this.state);
        if (Object.keys(this.state.errors).length === 0) {
            fetch(`${process.env.REACT_APP_API_URL}/template`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.state.customer)
            }).then(resp => resp.json())
                .then(res => console.log(res))
                .catch(error => console.log(error))
        }
    };

    checkRequired = () => {
        let errors = this.state.errors;
        if (this.state.customer.first_name === '') {
            errors.first_name = true
        }
        if (this.state.customer.last_name === '') {
            errors.last_name = true
        }
        if (this.state.customer.dob === '') {
            errors.dob = true
        }
        if (this.state.customer.mobile === '') {
            errors.mobile = true
        }
        if (this.state.customer.email === '') {
            errors.email = true
        }
        this.setState({errors: errors})
    };

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <h1>Landing Page Template</h1>
                </header>
                <div className="App-body">
                    <div className="layout">
                        <label id="first_name_label">First Name{this.state.errors.first_name ? <span>*</span> : ''}</label>
                        <input id="first_name_input" type="text" name="first_name" value={this.state.customer.first_name} onChange={this.inputChanged}/>
                        <label id="last_name_label">Last Name{this.state.errors.last_name ? <span>*</span> : ''}</label>
                        <input id="last_name_input" name="last_name" type="text" value={this.state.customer.last_name} onChange={this.inputChanged}/>
                        <label id="dob_name_label">Date of Birth{this.state.errors.dob ? <span>*</span> : ''}</label>
                        <input id="dob_input" name="dob" type="date" value={this.state.customer.dob} onChange={this.inputChanged}/>
                        <label id="mobile_label">Mobile Number{this.state.errors.mobile ? <span>*</span> : ''}</label>
                        <input id="mobile_input" name="mobile" type="tel" value={this.state.customer.mobile} onChange={this.inputChanged}/>
                        <label id="email_label">Email{this.state.errors.email ? <span>*</span> : ''}</label>
                        <input id="email_input" name="email" type="email" value={this.state.customer.email} onChange={this.inputChanged}/>
                        <label id="pdp_name_label">Preferred Departure Point</label>
                        <select id="pdp_input" name="pdp" value={this.state.customer.pdp} onChange={this.inputChanged}>
                            <option value="Auckland">Auckland</option>
                            <option value="Wellington">Wellington</option>
                            <option value="Christchurch">Christchurch</option>
                        </select>
                        {Object.keys(this.state.errors).length > 0 ? <h6 id='errors'>*Field cannot be blank</h6> : ''}
                    </div>
                    <br/>
                    <button className="submit" onClick={this.sendDetails}>Submit</button>
                </div>
            </div>
        );
    }
}

export default App;
