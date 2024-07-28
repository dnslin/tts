<template>
    <div class="tts p-4 bg-white rounded-lg shadow-lg">
        <h1 class="text-3xl font-bold mb-6 text-center text-blue-600">免费的文本转语音</h1>
        <el-form @submit.prevent="synthesize" label-width="100px" class="space-y-4">
            <el-form-item label="文本内容">
                <el-input type="textarea" v-model="text" required :autosize="{ minRows: 5, maxRows: 10 }"
                    class="custom-textarea" />
            </el-form-item>
            <el-form-item label="音色模型">
                <el-select v-model="voice" placeholder="选择一个音色">
                    <el-option v-for="voiceOption in voicesList" :key="voiceOption.name"
                        :label="`${voiceOption.language} - ${voiceOption.dialect} (${voiceOption.region}) - ${voiceOption.gender}`"
                        :value="voiceOption.name" />
                </el-select>
            </el-form-item>
            <el-form-item class="text-center">
                <el-button type="primary" @click="synthesize">请求转换</el-button>
            </el-form-item>
        </el-form>
        <div v-if="loading" class="mt-6 text-center ml-10">
            <el-progress :percentage="progress" status="active" show-text />
        </div>
        <div v-if="audioUrl && !loading" class="mt-6">
            <h2 class="text-xl font-semibold mb-2 text-center text-green-600">返回的语音内容:</h2>
            <audio :src="audioUrl" controls class="w-full rounded-md border border-gray-300"></audio>
            <div class="text-center mt-4">
                <el-button type="success" @click="downloadAudio">下载语音</el-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { voices } from '../data'
const text = ref('')
const voice = ref('zh-CN-XiaoxiaoNeural')
const audioUrl = ref(null)
const loading = ref(false)
const progress = ref(0)
const voicesList = ref(voices)

const synthesize = async () => {
    loading.value = true
    progress.value = 0
    try {
        const updateProgress = setInterval(() => {
            if (progress.value < 90) {
                progress.value += 10
            }
        }, 500)

        const response = await axios.post('http://127.0.0.1:8365/synthesize', {
            text: text.value,
            voice: voice.value
        }, {
            responseType: 'blob'
        })

        clearInterval(updateProgress)
        progress.value = 100

        const url = URL.createObjectURL(new Blob([response.data], { type: 'audio/mpeg' }))
        audioUrl.value = url
    } catch (error) {
        console.error('Error synthesizing speech:', error)
    } finally {
        loading.value = false
    }
}

const downloadAudio = () => {
    const link = document.createElement('a')
    link.href = audioUrl.value
    link.download = 'synthesized_audio.mp3'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
}
</script>

<style scoped>
.tts {
    max-width: 700px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: #f9fafb8c;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

:deep(.custom-textarea .el-input__inner) {
    font-size: 1rem;
    padding: 1rem;
    border-radius: 0.375rem;
    border: 1px solid #cbd5e0;
    resize: none;
    /* 禁用textarea的手动调整大小 */
}

:deep(.custom-textarea .el-input__inner::-webkit-scrollbar) {
    width: 8px;
}

:deep(.custom-textarea .el-input__inner::-webkit-scrollbar-thumb) {
    background-color: #a0aec0;
    border-radius: 4px;
}

:deep(.custom-textarea .el-input__inner::-webkit-scrollbar-track) {
    background-color: #edf2f7;
}

:deep(.el-form-item) {
    margin-bottom: 1.5rem;
}

:deep(.el-button) {
    width: 100%;
}

:deep(.el-progress) {
    width: 100%;
    border: none;
    /* 移除进度条的边框 */
}


:deep(.el-textarea__inner::-webkit-scrollbar) {
    width: 9px;
    height: 9px;
}

:deep(.el-textarea__inner::-webkit-scrollbar-track-piece) {
    background-color: #f8f8f8;
}

:deep(.el-textarea__inner::-webkit-scrollbar) {
    width: 9px;
    height: 9px;
}

:deep(.el-textarea__inner::-webkit-scrollbar-thumb) {
    background-color: #dddddd;
    background-clip: padding-box;
    min-height: 28px;
}

:deep(.el-textarea__inner::-webkit-scrollbar-thumb:hover) {
    background-color: #bbb;
}
</style>