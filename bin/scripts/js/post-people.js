import { People } from '../index.js.js'
console.log("HI",People);
for (const group in People) {
    for (const person in group) {
        const item = {
            "firstName": {"S": person.firstName},
            "middleName": {"S": person.middleName},
            "lastName": {"S": person.lastName},
            "phone": {"S": person.phone},
            "address": { 
                "M": {
                    "street": {"S": person.street},
                    "city": {"S": person.city},
                    "state": {"S": person.state},
                    "zip": {"S": person.zip}
                }
            },
            "birth": {"S": person.birth},
            "death": {"S": person.death},
            "relationship": {"S": person.relationship},
            "socialMedia": { 
                "M": {
                    "instagram": {"S": person.instagram},
                    "facebook": {"S": person.facebook},
                    "linkedIn":{"S":  person.linkedIn}
                }
            },
            "notes": { "L": person.notes}
        }
        console.log(item);
    }
}

console.log(P);
        const groups = Object.keys(P);
        for (const group of groups) {
            console.log("The group is:", group);

            for (const [index, person] of P[group].entries()) {
                console.log(group, index);
                const item = {
                    group: group,
                    id: index,
                    firstName: person.firstName,
                    middleName: person.middleName,
                    lastName: person.lastName,
                    mobile: person.mobile,
                    home: person.home,
                    email: person.email,
                    address: { 
                        street: person.address.street,
                        city: person.address.city,
                        state: person.address.state,
                        zip: person.address.zip
                    },
                    birth: person.birth,
                    death: person.death,
                    relationship: person.relationship,
                    socialMedia: { 
                        instagram: person.socialMedia.instagram,
                        facebook: person.socialMedia.facebook,
                        linkedIn: person.socialMedia.linkedIn
                    },
                    notes: person.notes,
                    operation: "create"
                }
                console.log("==>", JSON.stringify(item));
                fetch('https://vg534vly4d.execute-api.us-west-2.amazonaws.com/default/maCreatePerson', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(item)
        }).then( res => {
            console.log("SUCCESS!", res);
            return res.json();
        }).catch( err => {
            console.log(err);
        });
        //console.log(item);