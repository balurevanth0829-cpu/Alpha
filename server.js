const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Serve static files from the project root
app.use('/static', express.static(path.join(__dirname, 'static')));

// Serve the index.html for the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

// Serve the converter.html for the converter route
app.get('/converter', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'converter.html'));
});

// Serve the about.html for the about route
app.get('/about', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'about.html'));
});

function getTemperatureStatus(celsius) {
    if (celsius < -20) {
        return ["Extremely Cold", "Dangerously cold. Risk of frostbite."];
    } else if (celsius < 0) {
        return ["Very Cold", "Freezing temperatures. Make sure to bundle up!"];
    } else if (celsius < 10) {
        return ["Cold", "It's chilly outside. A warm jacket is recommended."];
    } else if (celsius < 20) {
        return ["Cool", "A mild and cool temperature. A light sweater is perfect."];
    } else if (celsius <= 28) {
        return ["Comfortable", `${Math.round(celsius)}°C is generally considered a very comfortable room temperature.`];
    } else if (celsius < 35) {
        return ["Warm", "It's getting warm. Stay hydrated and wear light clothing."];
    } else if (celsius < 40) {
        return ["Hot", "Hot weather! Avoid prolonged sun exposure during peak hours."];
    } else {
        return ["Extremely Hot", "Dangerously hot. Seek shade, stay indoors with AC, and drink plenty of water."];
    }
}

app.post('/api/convert', (req, res) => {
    try {
        let tempStr = req.body.temperature;
        if (tempStr === undefined || tempStr === null || tempStr.toString().trim() === '') {
            return res.status(400).json({ error: "Please enter a temperature value." });
        }
        
        let temp = parseFloat(tempStr);
        if (isNaN(temp)) {
            return res.status(400).json({ error: "Invalid temperature value. Please enter a valid number." });
        }

        let unit = req.body.unit;
        let c, f, k;

        if (unit === 'C') {
            c = temp;
            f = (c * 9/5) + 32;
            k = c + 273.15;
        } else if (unit === 'F') {
            f = temp;
            c = (f - 32) * 5/9;
            k = c + 273.15;
        } else if (unit === 'K') {
            if (temp < 0) {
                return res.status(400).json({ error: "Physically invalid. Temperature cannot be below Absolute Zero (0 K)." });
            }
            k = temp;
            c = k - 273.15;
            f = (c * 9/5) + 32;
        } else {
            return res.status(400).json({ error: "Invalid unit selected." });
        }

        if (k < 0) {
            // Address minor floating point precision issues
            k = Math.round(k * 1e10) / 1e10;
            if (k < 0) {
                return res.status(400).json({ error: "Temperature is below Absolute Zero (0 K) which is physically impossible." });
            }
        }

        const [status, insight] = getTemperatureStatus(c);

        res.json({
            C: Number(c.toFixed(2)),
            F: Number(f.toFixed(2)),
            K: Number(k.toFixed(2)),
            status: status,
            insight: insight,
            raw_c: c
        });

    } catch (error) {
        res.status(500).json({ error: "Internal server error." });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
