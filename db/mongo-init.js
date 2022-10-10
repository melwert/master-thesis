let piDb = "project_insight"

db = db.getSiblingDb(piDb);

db.createUser(
    {
        user: "pi",
        pwd: "",
        roles: [
            {
                role: "readWrite",
                db: piDb
            }
        ]
    }
);
