import html # pip install html
import uuid # pip install uuid
import streamlit as st # pip install streamlit

# função para injetar o código js no html através de um markdown
def inject_js_code(source: str) -> None:
    div_id = uuid.uuid4()

    st.markdown(
        f"""
    <div style="display:none" id="{div_id}">
        <iframe src="javascript: \
            var script = document.createElement('script'); \
            script.type = 'text/javascript'; \
            script.text = {html.escape(repr(source))}; \
            var div = window.parent.document.getElementById('{div_id}'); \
            div.appendChild(script); \
            div.parentElement.parentElement.parentElement.style.display = 'none'; \
        "/>
    </div>
    """,
        unsafe_allow_html=True,
    )
   
# função que adiciona EventListeners aos botões e cada vez que 1 é clicado é executado o código.
# o código é capaz de criar imagem, PDF e passar para a clipboard 
# é necessário gerar a imagem antes de gerar o PDF ou copiar para a clipboard
def screenshot_window() -> None:
  
    source = """

var button = document.getElementById('reportButton');

// se clicar no botão para gerar imagem então o código js é executado
button.addEventListener('click', function() {

    // função para carregar as bibliotecas através do script
    const loadScript = (url, isLoaded, callback) => {
        if (!isLoaded()) {
            const script = document.createElement('script');
            script.type = 'text/javascript';
            script.onload = callback;
            script.src = url;
            document.head.appendChild(script);
        } else {
            callback();
        }
    };

    // função para verificar se a biblioteca html2canvas está loaded
    const isHtml2CanvasLoaded = () => typeof html2canvas !== 'undefined';
    
    // função para verificar se a biblioteca jsPDF está loaded
    const isjsPDFLoaded = () => typeof jspdf !== 'undefined';

    // função para capturar uma iframe individual. Utilizada na função a seguir para capturar as várias iframes
    const captureIframe = (iframe, callback) => {

        try {
            const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
            html2canvas(iframeDoc.body, {
                scale: 1,
                logging: true,
                useCORS: true,
                allowTaint: true
            }).then(canvas => {
                callback(canvas ? canvas : null);

            }).catch(error => {
                console.error('Could not capture iframe:', error);
                callback(null);
            });
        } catch (error) {
            console.error('Could not access iframe:', error);
            callback(null);
        }
    };
    

    // função principal que vai capturar todas as iframes
    const captureAllWindows = () => {
        const streamlitDoc = window.parent.document;
        const stApp = streamlitDoc.querySelector('.main > .block-container');
        const iframes = Array.from(stApp.querySelectorAll('iframe'));

        let capturedImages = [];

        // capturar e processar cada iframe 
        const processIframes = (index = 0) => {
            if (index < iframes.length) {
                captureIframe(iframes[index], function(canvas) {
                    if (canvas) {
                        img = document.createElement('img');
                        img.src = canvas.toDataURL('image/png');
                        capturedImages.push({iframe: iframes[index], img: img});
                    } else {
                        console.error('Skipping an iframe due to capture failure.');
                    }
                    processIframes(index + 1);
                });
            } else {
                html2canvas(stApp, {
                    onclone: function(clonedDocument) {
                        const clonedIframes = Array.from(clonedDocument.querySelectorAll('iframe'));
                        capturedImages.forEach(({img}, index) => {
                            if (index < clonedIframes.length) {
                                const clonedIframe = clonedIframes[index];
                                clonedIframe.parentNode.replaceChild(img, clonedIframe);

                            }
                        });
                    },
                    scale: 1,
                    logging: true,
                    useCORS: true,
                    allowTaint: true,
                    ignoreElements: () => {}
                }).then(finalCanvas => {
                    window.finalCanvas = finalCanvas
                    
                    window.finalCanvas.toBlob(blob => {
                        // criação do download através do blob

                        const url = window.URL.createObjectURL(blob);
                        var link = document.createElement('a');
                        link.style.display = 'none';
                        link.href = url;
                        link.download = 'image.png';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        window.URL.revokeObjectURL(url);
                    });
                    
                }).catch(error => {
                    console.error('Screenshot capture failed:', error);
                });
            }
        };

        processIframes();
    };
    
    // primeira função a executar que irá desencadear todas as acima
    loadScript(
        'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.3.2/html2canvas.min.js',
        isHtml2CanvasLoaded,
        captureAllWindows
    );

    var buttonpdf = document.getElementById('pdfButton');

    // se clicar no botão para gerar PDF então o código js é executado
    buttonpdf.addEventListener('click', function() {

        // função que converte html canvas para pdf
        const convertToPDF = () => {

            const pdf = new jspdf.jsPDF('p', 'px', 'a4');

            const pageWidth = pdf.internal.pageSize.getWidth();
            const pageHeight = pdf.internal.pageSize.getHeight();

            const widthRatio = pageWidth / window.finalCanvas.width;
            const heightRatio = pageHeight / window.finalCanvas.height;
            const ratio = widthRatio > heightRatio ? heightRatio : widthRatio;

            const canvasWidth = window.finalCanvas.width * ratio;
            const canvasHeight = window.finalCanvas.height * ratio;
            
            pdf.addImage(window.finalCanvas, 'PNG', 0, 0, canvasWidth, canvasHeight);
            
            pdf.save('image-to-pdf.pdf');
        };

        // função que é chamada para dar load à biblioteca e que em seguida executa a função acima
        loadScript(
        'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
        isjsPDFLoaded,
        convertToPDF
        );

    });

    var buttonClipboard = document.getElementById('clipboardButton');
    buttonClipboard.addEventListener('click', function() {
        window.finalCanvas.toBlob((blob) => {
            const item = new ClipboardItem({ "image/png": blob });
            navigator.clipboard.write([item]);
        });
        
    });
});               
"""
    inject_js_code(source=source)  


# função para apresentar os botões 
def buttons():
    screenshot_window() # função chamada para definir o js <script> e injetar esse código no html

    # botões em html por causa do addEventListener por id
    st.sidebar.markdown(
        """
        <button class="st-style-button" id="reportButton">Gerar Imagem</button>
        """,
        unsafe_allow_html=True,
    )
    
    st.sidebar.markdown(
        """
        <button class="st-style-button" id="pdfButton">Gerar PDF</button>
        """,
        unsafe_allow_html=True,
    )     

    st.sidebar.markdown(
        """
        <button class="st-style-button" id="clipboardButton">Copiar para clipboard</button>
        """,
        unsafe_allow_html=True,
    ) 