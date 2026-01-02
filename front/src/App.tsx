import { useState, useRef } from 'react'
import { Send, Upload, FileText, Loader2, Bot, User, CheckCircle2, AlertCircle } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"

// API Base URL
const API_URL = "http://localhost:8000"

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: Source[]
  contexts?: string[] // For simple RAG
}

interface Source {
  source: string
  page: number
  content: string
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [uploadMessage, setUploadMessage] = useState('')

  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  
  // 'simple' or 'agentic'
  const [mode, setMode] = useState('simple')

  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setUploadStatus('idle')
      setUploadMessage('')
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setIsUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(`${API_URL}/ingest`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      
      if (!res.ok) throw new Error(data.detail || 'Upload failed')

      setUploadStatus('success')
      setUploadMessage(`Successfully ingested: ${data.filename} (${data.chunks_count} chunks)`)
    } catch (err: any) {
      console.error(err)
      setUploadStatus('error')
      setUploadMessage(err.message)
    } finally {
      setIsUploading(false)
    }
  }

  const handleChat = async () => {
    if (!query.trim()) return

    const userMsg: Message = { role: 'user', content: query }
    setMessages(prev => [...prev, userMsg])
    setQuery('')
    setIsLoading(true)

    try {
      const endpoint = mode === 'simple' ? '/chat/simple' : '/chat/agentic'
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg.content }),
      })
      const data = await res.json()

      if (!res.ok) throw new Error(data.detail || 'Chat failed')

      const assistantMsg: Message = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        contexts: data.contexts
      }
      setMessages(prev => [...prev, assistantMsg])
    } catch (err: any) {
      console.error(err)
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${err.message}` }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-4 max-w-5xl h-screen flex flex-col gap-4">
      <header className="flex items-center justify-between py-4 border-b">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Bot className="w-8 h-8" />
          RAG Evaluation Workbench
        </h1>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span>Server: {API_URL}</span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-[300px_1fr] gap-6 flex-1 overflow-hidden">
        {/* Sidebar: Upload & Settings */}
        <div className="flex flex-col gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Document Ingestion</CardTitle>
              <CardDescription>Upload PDF to RAG system</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid w-full max-w-sm items-center gap-1.5">
                <Input 
                  ref={fileInputRef}
                  id="pdf-upload" 
                  type="file" 
                  accept=".pdf"
                  onChange={handleFileChange} 
                />
              </div>
              <Button 
                onClick={handleUpload} 
                disabled={!file || isUploading} 
                className="w-full"
              >
                {isUploading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Upload className="mr-2 h-4 w-4" />}
                Ingest Document
              </Button>

              {uploadStatus === 'success' && (
                <div className="p-3 bg-green-50 text-green-700 rounded-md text-sm flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 mt-0.5" />
                  <span>{uploadMessage}</span>
                </div>
              )}
              {uploadStatus === 'error' && (
                <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 mt-0.5" />
                  <span>{uploadMessage}</span>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="flex-1 flex flex-col">
            <CardHeader>
              <CardTitle>System Status</CardTitle>
            </CardHeader>
            <CardContent className="flex-1">
              <div className="text-sm text-muted-foreground space-y-2">
                <p>Mode: <span className="font-semibold text-foreground capitalize">{mode} RAG</span></p>
                <p>Vector DB: <span className="font-semibold text-foreground">Chroma</span></p>
                <p>Embedding: <span className="font-semibold text-foreground">Gemini-001</span></p>
                <p>LLM: <span className="font-semibold text-foreground">Gemini-2.5-Flash</span></p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Chat Area */}
        <div className="flex flex-col h-full overflow-hidden border rounded-lg bg-background shadow-sm">
          <div className="p-4 border-b bg-muted/40">
            <Tabs value={mode} onValueChange={setMode} className="w-[400px]">
              <TabsList>
                <TabsTrigger value="simple">Simple RAG (Retrieve-Read)</TabsTrigger>
                <TabsTrigger value="agentic">Agentic RAG (LangGraph)</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50">
                <Bot className="w-16 h-16 mb-4" />
                <p>Upload a document and start chatting!</p>
              </div>
            )}
            
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-primary" />
                  </div>
                )}
                
                <div className={`max-w-[80%] space-y-2`}>
                  <div className={`p-3 rounded-lg ${
                    msg.role === 'user' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'bg-muted/50 border'
                  }`}>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                  </div>

                  {/* Sources Display for Assistant */}
                  {msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                    <div className="text-xs bg-card border rounded p-2 space-y-1">
                      <p className="font-semibold flex items-center gap-1 text-muted-foreground">
                        <FileText className="w-3 h-3" /> Sources:
                      </p>
                      <ul className="space-y-1">
                        {msg.sources.map((src, i) => (
                          <li key={i} className="text-muted-foreground">
                            <span className="font-medium text-foreground">{src.source}</span> (p.{src.page})
                            {/* <div className="pl-2 border-l-2 border-muted mt-1 opacity-75 line-clamp-2">"{src.content}"</div> */}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {msg.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5" />
                  </div>
                )}
              </div>
            ))}
            
            {isLoading && (
              <div className="flex gap-3">
                 <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <Bot className="w-5 h-5 text-primary" />
                  </div>
                  <div className="bg-muted/50 border p-3 rounded-lg flex items-center">
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    Thinking...
                  </div>
              </div>
            )}
          </div>

          <div className="p-4 border-t bg-background">
            <div className="flex gap-2">
              <Textarea 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleChat()
                  }
                }}
                placeholder="Ask a question about your documents..."
                className="min-h-[50px] max-h-[150px]"
              />
              <Button onClick={handleChat} disabled={isLoading || !query.trim()} className="h-auto">
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
