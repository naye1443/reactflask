import "../../Style/ImageList.css"
import {useEffect, useState} from "react";

const ImageList = ({userName}) => {
    const [images, setImages] = useState([])
    const [targetImage, setTargetImage] = useState(null)
    const [listItems, setListItems] = useState(null)

    useEffect(() => {
        getImages();
    }, []);

    const getImages = async () => {
        let owner = "test"

        await fetch("/files")
        .then(x => x.json())
        .then(x =>
        {
            setImages(x)
            setListItems(createList())
        })
    }

    const handleTargetImage = event => {
        setTargetImage(event.target.files[0])
    }

    const uploadImage = async event => {
        event.preventDefault()

        let user = "user"

        const formData = new FormData()
        formData.append('form_file', targetImage)
        formData.append('user', user)

        const response = await fetch('/upload', {
            method: 'POST',
            mode: 'cors',
            body: formData
        })

        const data = await response.json()

        if (data.status === 'success') {
            console.log('File uploaded successfully')
        } else {
            console.error('Error uploading file:', data.message)
        }

        await getImages()
    }

    const deleteImage = async (id, name) => {
        await fetch(`/delete?file_id=${name}`)

        await getImages()
    }

    const downloadImage = async (id, name) => {
        console.log(id)
        const response = await fetch(`/download?file_id=${name}`)

        console.log(response.headers)

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = name + '.jpeg';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
        else {
            console.log(`Error downloading image: ${response.status} ${response.statusText}`);
        }
    }

    const createList = () => {
        return (
            <div className="image-list">
                {images.map((image) => (
                    <div className = "image-grid">
                        <div className ="description-name">{image.name}</div>
                        <div className ="description-size">{image.size} kb</div>
                        <button className="button" onClick={() => downloadImage(image.id, image.name)}>DOWNLOAD</button>
                        <button className="button" onClick={() => deleteImage(image.id, image.name)}>DELETE</button>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="main-container">

            <div className="image-container">
                {listItems}
            </div>

            <br></br>

            <form className="upload-container" onSubmit={uploadImage}>
                <input type="file" onChange={handleTargetImage}/>
                <button type="submit">Upload</button>
            </form>

            <br></br>

            <div className="upload-container">
                <button className="update" onClick={() => getImages()}>UPDATE</button>
            </div>

            <br></br>

        </div>

    );
}
export default ImageList;
