import streamlit as st 

st.set_page_config(page_title="Unit Converter App", page_icon="🔄")


unit_categories = {
    "📏 Length": ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)", "Mile (mi)", "Yard (yd)", "Foot (ft)", "Inch (in)"],
    "⚖️ Mass": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Metric Ton (t)", "Pound (lb)", "Ounce (oz)"],
    "🌡️ Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
    "⏳ Time": ["Second (s)", "Millisecond (ms)", "Minute (min)", "Hour (h)", "Day (d)", "Week (wk)", "Month (mo)", "Year (yr)"],
    "🔁 Frequency": ["Hertz (Hz)", "Kilohertz (kHz)", "Megahertz (MHz)", "Gigahertz (GHz)"],
    "⚡ Energy": ["Joule (J)", "Kilojoule (kJ)", "Calorie (cal)", "Kilocalorie (kcal)", "Watt-hour (Wh)", "Kilowatt-hour (kWh)"],
    "💾 Digital Units": ["Bit (b)", "Byte (B)", "Kilobyte (KB)", "Megabyte (MB)", "Gigabyte (GB)", "Terabyte (TB)", "Petabyte (PB)"],
    "🧭 Pressure": ["Pascal (Pa)", "Kilopascal (kPa)", "Bar (bar)", "Atmosphere (atm)", "Pound per Square Inch (psi)"],
    "🚗 Speed": ["Meters per Second (m/s)", "Kilometers per Hour (km/h)", "Miles per Hour (mph)", "Feet per Second (ft/s)", "Knot (kn)"],
    "🛢️ Volume": ["Liter (L)", "Milliliter (mL)", "Cubic Meter (m³)", "Cubic Centimeter (cm³)", "Gallon (gal)", "Pint (pt)", "Cup"],
    "📐 Area": ["Square Meter (m²)", "Square Kilometer (km²)", "Square Centimeter (cm²)", "Square Foot (ft²)", "Square Inch (in²)", "Acre", "Hectare (ha)"],
    "🌀 Angle": ["Degree (°)", "Radian (rad)", "Gradian (gon)"]
}

unit_conversions = {
    "📏 Length": {  # Base unit: meter (m)
        "Meter (m)": 1,
        "Kilometer (km)": 0.001,
        "Centimeter (cm)": 100,
        "Millimeter (mm)": 1000,
        "Mile (mi)": 0.000621371,
        "Yard (yd)": 1.09361,
        "Foot (ft)": 3.28084,
        "Inch (in)": 39.3701
    },
    "⚖️ Mass": {  # Base unit: kilogram (kg)
        "Kilogram (kg)": 1,
        "Gram (g)": 1000,
        "Milligram (mg)": 1_000_000,
        "Metric Ton (t)": 0.001,
        "Pound (lb)": 2.20462,
        "Ounce (oz)": 35.274
    },
    "⏳ Time": {  # Base unit: second (s)
        "Second (s)": 1,
        "Millisecond (ms)": 1000,
        "Minute (min)": 1/60,
        "Hour (h)": 1/3600,
        "Day (d)": 1/86400,
        "Week (wk)": 1/604800,
        "Month (mo)": 1/2.628e+6,  # Approximate (30.44 days)
        "Year (yr)": 1/3.154e+7   # Approximate (365.25 days)
    },
    "🔁 Frequency": {  # Base unit: Hertz (Hz)
        "Hertz (Hz)": 1,
        "Kilohertz (kHz)": 0.001,
        "Megahertz (MHz)": 0.000001,
        "Gigahertz (GHz)": 0.000000001
    },
    "⚡ Energy": {  # Base unit: Joule (J)
        "Joule (J)": 1,
        "Kilojoule (kJ)": 0.001,
        "Calorie (cal)": 0.239006,
        "Kilocalorie (kcal)": 0.000239006,
        "Watt-hour (Wh)": 0.000277778,
        "Kilowatt-hour (kWh)": 2.77778e-7
    },
    "💾 Digital Units": {  # Base unit: Bit (b)
        "Bit (b)": 1,
        "Byte (B)": 1/8,
        "Kilobyte (KB)": 1/8_000,
        "Megabyte (MB)": 1/8_000_000,
        "Gigabyte (GB)": 1/8_000_000_000,
        "Terabyte (TB)": 1/8_000_000_000_000,
        "Petabyte (PB)": 1/8_000_000_000_000_000
    },
    "🧭 Pressure": {  # Base unit: Pascal (Pa)
        "Pascal (Pa)": 1,
        "Kilopascal (kPa)": 0.001,
        "Bar (bar)": 1e-5,
        "Atmosphere (atm)": 9.8692e-6,
        "Pound per Square Inch (psi)": 0.000145038
    },
    "🚗 Speed": {  # Base unit: Meters per Second (m/s)
        "Meters per Second (m/s)": 1,
        "Kilometers per Hour (km/h)": 3.6,
        "Miles per Hour (mph)": 2.23694,
        "Feet per Second (ft/s)": 3.28084,
        "Knot (kn)": 1.94384
    },
    "🛢️ Volume": {  # Base unit: Liter (L)
        "Liter (L)": 1,
        "Milliliter (mL)": 1000,
        "Cubic Meter (m³)": 0.001,
        "Cubic Centimeter (cm³)": 1000,
        "Gallon (gal)": 0.264172,
        "Pint (pt)": 2.11338,
        "Cup": 4.16667
    },
    "📐 Area": {  # Base unit: Square Meter (m²)
        "Square Meter (m²)": 1,
        "Square Kilometer (km²)": 0.000001,
        "Square Centimeter (cm²)": 10_000,
        "Square Foot (ft²)": 10.7639,
        "Square Inch (in²)": 1550,
        "Acre": 0.000247105,
        "Hectare (ha)": 0.0001
    },
    "🌀 Angle": {  # Base unit: Degree (°)
        "Degree (°)": 1,
        "Radian (rad)": 0.0174533,
        "Gradian (gon)": 1.11111
    }
}


def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    elif from_unit == "Celsius (°C)":
        if to_unit == "Fahrenheit (°F)":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin (K)":
            return value + 273.15
    elif from_unit == "Fahrenheit (°F)":
        if to_unit == "Celsius (°C)":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin (K)":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin (K)":
        if to_unit == "Celsius (°C)":
            return value - 273.15
        elif to_unit == "Fahrenheit (°F)":
            return (value - 273.15) * 9/5 + 32


def convert_unit(value  , from_unit , to_unit , conversion_type):
    if conversion_type == "🌡️ Temperature":
        return convert_temperature(value, from_unit, to_unit)
    
    from_unit_conversion_rate = unit_conversions[conversion_type][from_unit]
    to_unit_conversion_rate = unit_conversions[conversion_type][to_unit]
    base_value = value / from_unit_conversion_rate
    output = base_value * to_unit_conversion_rate
    return output

if "history" not in st.session_state:
    st.session_state.history = []




st.sidebar.header("📌 Select Conversion Type")
conversion_type = st.sidebar.selectbox(
    "Choose a category",
    [
        "📏 Length",
        "⚖️ Mass",
        "🌡️ Temperature",
        "⏳ Time",
        "🔁 Frequency",
        "⚡ Energy",
        "💾 Digital Units",
        "🧭 Pressure",
        "🚗 Speed",
        "🛢️ Volume",
        "📐 Area",
        "🌀 Angle"
    ]
)



st.title("🤖 Huza Unit Converter")
st.write("🔄 Convert Anything, Anytime  Your Ultimate Unit Converter! ⚡")

input_value = st.number_input("🔢Enter Value here")
from_unit = st.selectbox("📍 From Unit",unit_categories[conversion_type])
to_unit = st.selectbox("🎯 To Unit",unit_categories[conversion_type])

if st.button("Convert"):
    result = convert_unit(input_value,from_unit,to_unit,conversion_type)
    st.success(f"🎉Result: {result}")
    st.session_state.history.append({"Value": input_value, "From": from_unit, "To": to_unit, "Result": result})
if st.sidebar.button("📜 Show History"):
    st.write("📜 **Conversion History**")
    st.table(st.session_state.history)
if st.sidebar.button("❌ Clear History"):
    st.session_state.history = []
    
    
st.write("Created By Huzaifa Younus 🎉")



