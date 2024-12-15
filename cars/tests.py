from django.test import TestCase
from cars.models import Car, Drive, EngineType, BodyType, TransmissionType
from rest_framework.test import APIClient
from model_bakery import baker

# Create your tests here.
 
##############Тест модели Car###############
class CarsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        dr = baker.make("cars.Drive")
        car = baker.make("Car", drive = dr)
        
        r = self.client.get('/api/cars/')
        data = r.json()
        print(data)
        
        assert car.name == data[0]['name']
        assert car.id == data[0]["id"]
        assert car.drive.name == data[0]["drive"]['name']
        assert car.drive.id == data[0]["drive"]['id']
        assert len(data) == 1
        
    def test_careate_car(self):
        dr = baker.make("cars.Drive")
        
        r = self.client.post("/api/cars/", {
            "name" : "Авто",
            "drive" : dr.id
        })
        
        new_car_id = r.json()['id']
        cars = Car.objects.all()
        assert len(cars) == 1
        
        new_car = Car.objects.filter(id = new_car_id).first()
        assert new_car.name == 'Авто'
        assert new_car.drive == dr
        
    def test_delete_car(self):
        cars = baker.make("Car", 10)
        r = self.client.get('/api/cars/')
        data = r.json()
        assert len(data) == 10
        
        car_id_to_delete = cars[3].id
        self.client.delete(f'/api/cars/{car_id_to_delete}/')
        
        r = self.client.get('/api/cars/')
        data = r.json()
        assert len(data) == 9
        assert car_id_to_delete not in [i['id'] for i in data]
        
    def test_update_car(self):
        cars = baker.make("Car", 10)
        car: Car = cars[2]
        
        r = self.client.get(f'/api/cars/{car.id}/')
        data = r.json()
        assert data['name'] == car.name
        
        r = self.client.put(f'/api/cars/{car.id}/', {
            "name" : "Honda NSX"
        })
        assert r.status_code == 200
        
        r = self.client.get(f'/api/cars/{car.id}/')
        data = r.json()
        assert data['name'] == "Honda NSX"
        
        car.refresh_from_db()
        assert data['name'] == car.name
        
    def test_update_drive(self):
        drives = baker.make("Drive", 10)
        drive: Drive = drives[2]
        
        r = self.client.get(f'/api/drives/{drive.id}/')
        data = r.json()
        assert data['name'] == drive.name
        
        r = self.client.put(f'/api/drives/{drive.id}/', {
            "name": "RWD"
        })  
        
        assert r.status_code == 200  
        
        r = self.client.get(f'/api/drives/{drive.id}/')
        data = r.json()
        assert data['name'] == "RWD"
        
        drive.refresh_from_db()
        assert data['name'] == drive.name


###################Тест модели Drive########################    
class DriveViewsetTestCase(TestCase): 
    def setUp(self):
        self.client = APIClient()
    def test_get_drive_list(self):
        drives = baker.make("Drive", _quantity=5)
        
        r = self.client.get('/api/drives/')
        data = r.json()
        
        assert len(data) == 5  
        assert all(d['id'] in [drive.id for drive in drives] for d in data) 
        
    def test_create_drive(self):
        r = self.client.post('/api/drives/', {
            "name": "AWD"
        })
        
        assert r.status_code == 201  
        new_drive_id = r.json()['id']
        
        new_drive = Drive.objects.filter(id=new_drive_id).first()
        assert new_drive.name == "AWD"
        
    def test_update_drive(self):
        drives = baker.make("Drive", 10)
        drive: Drive = drives[2]
        
        r = self.client.get(f'/api/drives/{drive.id}/')
        data = r.json()
        assert data['name'] == drive.name
        
        r = self.client.put(f'/api/drives/{drive.id}/', {
            "name": "RWD"
        })  
        assert r.status_code == 200  
        
        r = self.client.get(f'/api/drives/{drive.id}/')
        data = r.json()
        assert data['name'] == "RWD"
        
        drive.refresh_from_db()
        assert data['name'] == drive.name
        
    def test_delete_drive(self):
        drives = baker.make("Drive", 10)
        r = self.client.get('/api/drives/')
        data = r.json()
        assert len(data) == 10
        
        drive_id_to_delete = drives[3].id
        self.client.delete(f'/api/drives/{drive_id_to_delete}/')
        
        r = self.client.get('/api/drives/')
        data = r.json()
        assert len(data) == 9
        assert drive_id_to_delete not in [i['id'] for i in data]
        
###################Тест модели EngineType########################    
class EngineViewsetTestCase(TestCase): 
    def setUp(self):
        self.client = APIClient()
    def test_get_enginetype_list(self):
        ets = baker.make("EngineType", _quantity=5)
        
        r = self.client.get('/api/enginetypes/')
        data = r.json()
        
        assert len(data) == 5  
        assert all(d['id'] in [et.id for et in ets] for d in data) 
        
    def test_create_enginetype(self):
        r = self.client.post('/api/enginetypes/', {
            "etype": "Рядное"
        })
        
        assert r.status_code == 201  
        new_etype_id = r.json()['id']
        
        new_etype = EngineType.objects.filter(id=new_etype_id).first()
        assert new_etype.etype == "Рядное"
        
    def test_update_enginetype(self):
        enginetypes = baker.make("EngineType", 10)
        enginetype: EngineType = enginetypes[2]
        
        r = self.client.get(f'/api/enginetypes/{enginetype.id}/')
        data = r.json()
        assert data['etype'] == enginetype.etype
        
        r = self.client.put(f'/api/enginetypes/{enginetype.id}/', {
            "etype": "Оппозитный"
        })  
        assert r.status_code == 200  
        
        r = self.client.get(f'/api/enginetypes/{enginetype.id}/')
        data = r.json()
        assert data['etype'] == "Оппозитный"
        
        enginetype.refresh_from_db()
        assert data['etype'] == enginetype.etype
        
    def test_delete_enginetype(self):
        enginetypes = baker.make("EngineType", 10)
        r = self.client.get('/api/enginetypes/')
        data = r.json()
        assert len(data) == 10
        
        enginetype_id_to_delete = enginetypes[3].id
        self.client.delete(f'/api/enginetypes/{enginetype_id_to_delete}/')
        
        r = self.client.get('/api/enginetypes/')
        data = r.json()
        assert len(data) == 9
        assert enginetype_id_to_delete not in [i['id'] for i in data]
        
###################Тест модели BodyType########################    
class BodyViewsetTestCase(TestCase): 
    def setUp(self):
        self.client = APIClient()
    def test_get_bodytype_list(self):
        bts = baker.make("BodyType", _quantity=5) #bts от слова Bodytypes
        
        r = self.client.get('/api/bodytypes/')
        data = r.json()
        
        assert len(data) == 5  
        assert all(d['id'] in [bt.id for bt in bts] for d in data) 
        
    def test_create_bodytype(self):
        r = self.client.post('/api/bodytypes/', {
            "btype": "Седан"
        })
        
        assert r.status_code == 201  
        new_btype_id = r.json()['id']
        
        new_btype = BodyType.objects.filter(id=new_btype_id).first()
        assert new_btype.btype == "Седан"
        
    def test_update_bodytype(self):
        bodytypes = baker.make("BodyType", 10)
        bodytype: BodyType = bodytypes[2]
        
        r = self.client.get(f'/api/bodytypes/{bodytype.id}/')
        data = r.json()
        assert data['btype'] == bodytype.btype
        
        r = self.client.put(f'/api/bodytypes/{bodytype.id}/', {
            "btype": "V-образный"
        })  
        assert r.status_code == 200  
        
        r = self.client.get(f'/api/bodytypes/{bodytype.id}/')
        data = r.json()
        assert data['btype'] == "V-образный"
        
        bodytype.refresh_from_db()
        assert data['btype'] == bodytype.btype
        
    def test_delete_bodytype(self):
        bodytypes = baker.make("BodyType", 10)
        r = self.client.get('/api/bodytypes/')
        data = r.json()
        assert len(data) == 10
        
        bodytype_id_to_delete = bodytypes[3].id
        self.client.delete(f'/api/bodytypes/{bodytype_id_to_delete}/')
        
        r = self.client.get('/api/bodytypes/')
        data = r.json()
        assert len(data) == 9
        assert bodytype_id_to_delete not in [i['id'] for i in data]
        
###################Тест модели TransmissionType########################    
class TransmissionViewsetTestCase(TestCase): 
    def setUp(self):
        self.client = APIClient()
    def test_get_transmissiontype_list(self):
        trts = baker.make("TransmissionType", _quantity=5) 
        
        r = self.client.get('/api/transmissiontypes/')
        data = r.json()
        
        assert len(data) == 5  
        assert all(d['id'] in [trt.id for trt in trts] for d in data) 
        
    def test_create_transmissiontype(self):
        r = self.client.post('/api/transmissiontypes/', {
            "trtype": "АКПП"
        })
        
        assert r.status_code == 201  
        new_trtype_id = r.json()['id']
        
        new_trtype = TransmissionType.objects.filter(id=new_trtype_id).first()
        assert new_trtype.trtype == "АКПП"
        
    def test_update_transmissiontype(self):
        transmissiontypes = baker.make("TransmissionType", 10)
        transmissiontype: TransmissionType = transmissiontypes[2]
        
        r = self.client.get(f'/api/transmissiontypes/{transmissiontype.id}/')
        data = r.json()
        assert data['trtype'] == transmissiontype.trtype
        
        r = self.client.put(f'/api/transmissiontypes/{transmissiontype.id}/', {
            "trtype": "МКПП"
        })  
        assert r.status_code == 200  
        
        r = self.client.get(f'/api/transmissiontypes/{transmissiontype.id}/')
        data = r.json()
        assert data['trtype'] == "МКПП"
        
        transmissiontype.refresh_from_db()
        assert data['trtype'] == transmissiontype.trtype
        
    def test_delete_transmissiontype(self):
        transmissiontypes = baker.make("TransmissionType", 10)
        r = self.client.get('/api/transmissiontypes/')
        data = r.json()
        assert len(data) == 10
        
        transmission_id_to_delete = transmissiontypes[3].id
        self.client.delete(f'/api/transmissiontypes/{transmission_id_to_delete}/')
        
        r = self.client.get('/api/transmissiontypes/')
        data = r.json()
        assert len(data) == 9
        assert transmission_id_to_delete not in [i['id'] for i in data]