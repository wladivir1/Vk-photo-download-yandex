import requests
import json
from tqdm import tqdm  # библиотека для создания прогресс-бара
import datetime


class VKPhotosGet:
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.y_token = y_token
        self.base_url = 'https://api.vk.com/method/'
        
    def _get_photos(self):
        """Делает запрос на страницу VK и возвращает данные по фотографиям"""
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 5,  # установливаем нужное количество фото для загрузки
            'v': '5.131',
            'access_token': self.access_token
        }
        response = requests.get(self.base_url + 'photos.get', params=params)
        data = response.json()['response']['items']
        
        return data
    
    def list_vk_photo(sef):
        """Получает: количество лайков, дату, url фотографии со страницы
           и записывает информациюв словарь. """
        data = vk_photos._get_photos()
        list_photo = []
        
        for photo in data:
            # сортируем фотографии по height в обратном порядке
            max_size_photo = sorted(photo['sizes'], key=lambda x: x['height'], reverse=True)
            for size_photo in max_size_photo:
                url_photo = size_photo['url']
                likes = photo['likes']['count']
                # Получаем дату фотографии
                date = datetime.datetime.fromtimestamp(photo["date"]).strftime('%Y.%m.%d')
                                               
            dict_photo ={'likes': likes, 'date': date, 'url': url_photo}
            list_photo.append(dict_photo)
            
        return list_photo
     
    def backup_photos(self):
        photo_data = vk_photos._get_photos()           
        list_backup_info = []
        
        for photo in photo_data:
            likes = photo['likes']['count']            
            for size in photo['sizes']:
                types = size['type']
            name = f'{likes}.jpg'
            #Сохранение информации о фотографии
            backup_info = {'file_name': name, 'size': types}
            list_backup_info.append(backup_info)
            
        return list_backup_info    
         
    def download_file_json(self):
        """Сохранение информации о фотографиях в JSON-файл"""
        list_backup_info = vk_photos.backup_photos()    
        with open('backup_info.json', 'w') as file:
            json.dump(list_backup_info, file, indent=4)
                
    
class YandexDownloader:
    def __init__(self, y_token, vk_photos):
        self.y_token = y_token
        self.vk_photos = vk_photos
        self.headers = {'Authorization': 'OAuth ' + self.y_token }
        
    def folder_creation(self):
        params = {
            'path': 'photo'
        }
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=self.headers, params=params)
        if response.status_code == 201:
            print('Папка photo успешно создана на Яндекс.Диске')    
        
    def download_photos(self):
        list_photo = self.vk_photos.list_vk_photo()       
        checked_likes = set()
        # tqdm прогресс-бар для загрузки фото
        for photo_name in tqdm(list_photo, desc='Download photo'):
            date = photo_name['date']
            likes = photo_name['likes']
            if likes in checked_likes:
                continue
            # Сравниваем одинаковое количество лайков
            count = sum(1 for p in list_photo if p['likes'] == likes)                   
            if count > 1:
                name = (f'{date} {likes}.jpg')
            else:
                name = (f'{likes}.jpg')    
            checked_likes.add(likes)
            # загружаем фотографии на яндекс диск    
            params = {
                    'url': photo_name['url'],
                    'path': '/photo/' + name,
                    }
            response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=self.headers, params=params)

                        
if __name__ == '__main__':
    user_id = input('Введите ID пользователя VK: ')
    y_token = input('Введите токен с Полигона Яндекс.Диска: ')
    access_token = open('access_token', encoding='utf-8').read()
    
    vk_photos = VKPhotosGet(user_id, access_token)
    y_download = YandexDownloader(y_token, vk_photos)
    y_download.folder_creation()
    y_download.download_photos()
    vk_photos._get_photos()
    vk_photos.list_vk_photo()
    vk_photos.backup_photos()
    vk_photos.download_file_json()
    