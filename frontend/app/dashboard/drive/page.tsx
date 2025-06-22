"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Upload, File, Calendar } from "lucide-react"
import axios from "@/lib/axios"

interface UploadedFile {
  id: string
  name: string
  size: string
  uploadDate: string
}

// dummy
const dummyFiles: UploadedFile[] = [
  {
    id: "1",
    name: "project-proposal.pdf",
    size: "2.4 MB",
    uploadDate: "2024-01-15",
  },
  {
    id: "2",
    name: "research-paper.docx",
    size: "1.8 MB",
    uploadDate: "2024-01-14",
  },
  {
    id: "3",
    name: "meeting-notes.txt",
    size: "45 KB",
    uploadDate: "2024-01-13",
  },
]

export default function DrivePage() {
  const [files, setFiles] = useState<UploadedFile[]>(dummyFiles)
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [message, setMessage] = useState("")

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files)
    }
  }, [])

  const handleFiles = async (fileList: FileList) => {
    setUploading(true)
    setMessage("")

    try {
      const formData = new FormData()
      Array.from(fileList).forEach((file) => {
        formData.append("files", file)
      })

      const response = await axios.post("/api/file/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      });

      if (response.status === 200) {
        setMessage("Files uploaded successfully!")
        //dummy
        const newFiles = Array.from(fileList).map((file, index) => ({
          id: Date.now().toString() + index,
          name: file.name,
          size: `${(file.size / 1024 / 1024).toFixed(1)} MB`,
          uploadDate: new Date().toISOString().split("T")[0],
        }))
        setFiles((prev) => [...newFiles, ...prev])
      } else {
        setMessage("Upload failed. Please try again.")
      }
    } catch (error) {
      setMessage("Network error occurred during upload.")
    } finally {
      setUploading(false)
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFiles(e.target.files)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Document Drive</h2>
        <p className="text-gray-600">Upload and manage your documents for Q&A</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upload Documents</CardTitle>
          <CardDescription>Drag and drop files here or click to browse</CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400"
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <div className="space-y-2">
              <p className="text-lg font-medium">{dragActive ? "Drop files here" : "Upload your documents"}</p>
              <p className="text-sm text-gray-500">Supports PDF, DOC, DOCX, TXT files</p>
            </div>
            <div className="mt-4">
              <Input
                type="file"
                multiple
                accept=".pdf,.doc,.docx,.txt"
                onChange={handleFileInput}
                className="hidden"
                id="file-upload"
              />
              <Button asChild disabled={uploading}>
                <label htmlFor="file-upload" className="cursor-pointer">
                  {uploading ? "Uploading..." : "Browse Files"}
                </label>
              </Button>
            </div>
          </div>
          {message && (
            <Alert className="mt-4">
              <AlertDescription>{message}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Uploaded Documents</CardTitle>
          <CardDescription>
            {files.length} document{files.length !== 1 ? "s" : ""} available for Q&A
          </CardDescription>
        </CardHeader>
        <CardContent>
          {files.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No documents uploaded yet</div>
          ) : (
            <div className="space-y-3">
              {files.map((file) => (
                <div key={file.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                  <div className="flex items-center space-x-3">
                    <File className="h-5 w-5 text-blue-500" />
                    <div>
                      <p className="font-medium">{file.name}</p>
                      <p className="text-sm text-gray-500">{file.size}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-500">
                    <Calendar className="h-4 w-4" />
                    <span>{file.uploadDate}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
