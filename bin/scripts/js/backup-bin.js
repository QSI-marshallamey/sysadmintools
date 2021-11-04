const { exec } = require("child_process");

exec("rsync -avh --delete ~/bin/ '/Users/marshallamey/pCloud Drive/Projects/bin' >> ~/backup.log", (error, stdout, stderr) => {
    if (error) {
        console.log(`error: ${error.message}`);
        return;
    }
    if (stderr) {
        console.log(`stderr: ${stderr}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
});
