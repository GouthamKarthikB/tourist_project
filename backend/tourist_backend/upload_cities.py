import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tourist_backend.settings")
django.setup()

from users.models import State, City

INDIAN_STATES_CITIES = {
    "Andhra Pradesh": [
        "Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Nellore",
        "Kakinada", "Rajahmundry", "Kadapa", "Anantapur", "Eluru"
    ],
    "Arunachal Pradesh": [
        "Itanagar", "Tawang", "Ziro", "Pasighat", "Bomdila",
        "Naharlagun", "Roing", "Along", "Daporijo", "Tezu"
    ],
    "Assam": [
        "Guwahati", "Dibrugarh", "Tezpur", "Jorhat", "Silchar",
        "Nagaon", "Tinsukia", "Bongaigaon", "Diphu", "Karimganj"
    ],
    "Bihar": [
        "Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga",
        "Purnia", "Arrah", "Bettiah", "Chapra", "Katihar"
    ],
    "Chhattisgarh": [
        "Raipur", "Bilaspur", "Durg", "Bhilai", "Korba",
        "Jagdalpur", "Rajnandgaon", "Raigarh", "Ambikapur", "Dhamtari"
    ],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"],
    "Gujarat": [
        "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar",
        "Bhavnagar", "Jamnagar", "Junagadh", "Anand", "Nadiad"
    ],
    "Haryana": [
        "Gurgaon", "Faridabad", "Panipat", "Ambala", "Karnal",
        "Rohtak", "Hisar", "Yamunanagar", "Sonipat", "Bhiwani"
    ],
    "Himachal Pradesh": [
        "Shimla", "Manali", "Dharamshala", "Kullu", "Solan",
        "Mandi", "Chamba", "Hamirpur", "Bilaspur", "Kangra"
    ],
    "Jharkhand": [
        "Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar",
        "Hazaribagh", "Giridih", "Ramgarh", "Medininagar", "Chaibasa"
    ],
    "Karnataka": [
        "Bangalore", "Mysore", "Mangalore", "Hubli", "Belgaum",
        "Davangere", "Tumkur", "Bijapur", "Gulbarga", "Shivamogga"
    ],
    "Kerala": [
        "Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam",
        "Alappuzha", "Palakkad", "Kannur", "Malappuram", "Kottayam"
    ],
    "Madhya Pradesh": [
        "Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain",
        "Sagar", "Rewa", "Satna", "Ratlam", "Dewas"
    ],
    "Maharashtra": [
        "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad",
        "Solapur", "Amravati", "Thane", "Kolhapur", "Sangli"
    ],
    "Manipur": ["Imphal", "Bishnupur", "Thoubal", "Churachandpur", "Ukhrul"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Baghmara", "Nongpoh"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Kolasib", "Saiha"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha"],
    "Odisha": [
        "Bhubaneswar", "Cuttack", "Puri", "Rourkela", "Sambalpur",
        "Berhampur", "Balasore", "Baripada", "Jharsuguda", "Kendrapara"
    ],
    "Punjab": [
        "Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda",
        "Mohali", "Pathankot", "Hoshiarpur", "Moga", "Firozpur"
    ],
    "Rajasthan": [
        "Jaipur", "Udaipur", "Jodhpur", "Kota", "Ajmer",
        "Bikaner", "Alwar", "Bharatpur", "Sikar", "Chittorgarh"
    ],
    "Sikkim": ["Gangtok", "Namchi", "Mangan", "Gyalshing", "Ravangla"],
    "Tamil Nadu": [
        "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem",
        "Erode", "Vellore", "Tirunelveli", "Thoothukudi", "Dindigul"
    ],
    "Telangana": [
        "Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam",
        "Ramagundam", "Siddipet", "Mahbubnagar", "Adilabad", "Mancherial"
    ],
    "Tripura": ["Agartala", "Dharmanagar", "Udaipur", "Kailashahar", "Belonia"],
    "Uttar Pradesh": [
        "Lucknow", "Kanpur", "Agra", "Varanasi", "Prayagraj",
        "Meerut", "Bareilly", "Ghaziabad", "Gorakhpur", "Aligarh"
    ],
    "Uttarakhand": [
        "Dehradun", "Haridwar", "Nainital", "Mussoorie", "Rishikesh",
        "Haldwani", "Almora", "Pithoragarh", "Rudrapur", "Kashipur"
    ],
    "West Bengal": [
        "Kolkata", "Darjeeling", "Siliguri", "Durgapur", "Howrah",
        "Asansol", "Malda", "Kharagpur", "Haldia", "Bardhaman"
    ],
    "Andaman and Nicobar Islands": ["Port Blair"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Silvassa"],
    "Lakshadweep": ["Kavaratti"],
    "Delhi": ["New Delhi", "Central Delhi", "South Delhi", "East Delhi", "West Delhi"],
    "Puducherry": ["Puducherry", "Karaikal", "Yanam", "Mahe"],
    "Ladakh": ["Leh", "Kargil"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Udhampur"]
}


def upload_states_and_cities():
    for state_name, cities in INDIAN_STATES_CITIES.items():
        state, _ = State.objects.get_or_create(name=state_name)
        for city_name in cities:
            City.objects.get_or_create(name=city_name, state=state)
    print("✅ Data uploaded successfully!")

upload_states_and_cities()
